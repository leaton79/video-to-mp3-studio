from __future__ import annotations

import os
import sys
import threading
import uuid
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from downloader import ConversionError, ToolMissingError, start_conversion
from validators import ALLOWED_BITRATES, validate_filename, validate_url


if getattr(sys, "frozen", False):
    APP_ROOT = Path(sys.executable).resolve().parents[1]
    RESOURCES_DIR = APP_ROOT / "Resources"
    DOWNLOADS_DIR = Path.home() / "Downloads" / "Video to MP3 Studio"
    COOKIES_DIR = Path.home() / "Documents" / "Video to MP3 Studio"
else:
    RESOURCES_DIR = Path(__file__).resolve().parent
    DOWNLOADS_DIR = RESOURCES_DIR / "downloads"
    COOKIES_DIR = RESOURCES_DIR / "cookies"


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(RESOURCES_DIR / "templates"),
        static_folder=str(RESOURCES_DIR / "static"),
    )
    app.config["DOWNLOADS_DIR"] = DOWNLOADS_DIR
    app.config["COOKIES_DIR"] = COOKIES_DIR
    app.config["JOBS"] = {}
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 32

    DOWNLOADS_DIR.mkdir(exist_ok=True)
    COOKIES_DIR.mkdir(parents=True, exist_ok=True)

    @app.get("/")
    def index():
        return render_template("index.html", bitrates=ALLOWED_BITRATES)

    @app.get("/api/health")
    def health():
        ffmpeg_found = bool(_which("ffmpeg"))
        yt_dlp_cli_found = bool(_which("yt-dlp"))
        youtube_cookies_found = (COOKIES_DIR / "youtube-cookies.txt").exists()
        return jsonify(
            {
                "status": "ok",
                "tools": {
                    "ffmpeg": ffmpeg_found,
                    "yt_dlp": yt_dlp_cli_found,
                    "yt_dlp_cli": yt_dlp_cli_found,
                    "youtube_cookies": youtube_cookies_found,
                },
            }
        )

    @app.post("/api/jobs")
    def create_job():
        payload = request.get_json(silent=True) or {}
        video_url = (payload.get("video_url") or "").strip()
        output_name = (payload.get("output_name") or "").strip()
        bitrate = str(payload.get("bitrate") or "").strip()

        url_error = validate_url(video_url)
        name_error = validate_filename(output_name)
        bitrate_error = None if bitrate in ALLOWED_BITRATES else "Choose a supported bitrate."

        if url_error or name_error or bitrate_error:
            return (
                jsonify(
                    {
                        "error": "Please fix the highlighted fields.",
                        "field_errors": {
                            "video_url": url_error,
                            "output_name": name_error,
                            "bitrate": bitrate_error,
                        },
                    }
                ),
                400,
            )

        job_id = uuid.uuid4().hex
        destination = app.config["DOWNLOADS_DIR"] / f"{output_name}.mp3"
        app.config["JOBS"][job_id] = {
            "id": job_id,
            "status": "queued",
            "message": "Your conversion is queued.",
            "progress": 0.0,
            "output_name": output_name,
            "bitrate": bitrate,
            "video_url": video_url,
            "file_path": str(destination),
            "download_url": None,
            "error": None,
        }

        thread = threading.Thread(
            target=_run_job,
            args=(app, job_id, video_url, output_name, bitrate),
            daemon=True,
        )
        thread.start()

        return jsonify({"job_id": job_id}), 202

    @app.get("/api/jobs/<job_id>")
    def get_job(job_id: str):
        job = app.config["JOBS"].get(job_id)
        if not job:
            return jsonify({"error": "Job not found."}), 404
        return jsonify(job)

    return app


def _run_job(app: Flask, job_id: str, video_url: str, output_name: str, bitrate: str) -> None:
    with app.app_context():
        jobs = app.config["JOBS"]
        job = jobs[job_id]

        def update(status: str, message: str, progress: float | None = None) -> None:
            job["status"] = status
            job["message"] = message
            if progress is not None:
                job["progress"] = max(0.0, min(progress, 100.0))

        update("running", "Starting download tools check...", 2)

        try:
            file_path = start_conversion(
                video_url=video_url,
                output_name=output_name,
                bitrate=bitrate,
                downloads_dir=app.config["DOWNLOADS_DIR"],
                cookies_dir=app.config["COOKIES_DIR"],
                progress_callback=update,
            )
        except ToolMissingError as exc:
            job["status"] = "failed"
            job["error"] = str(exc)
            job["message"] = str(exc)
            job["progress"] = 0.0
        except ConversionError as exc:
            job["status"] = "failed"
            job["error"] = str(exc)
            job["message"] = str(exc)
            job["progress"] = 0.0
        except Exception:
            job["status"] = "failed"
            job["error"] = "Unexpected error while converting the file."
            job["message"] = "Unexpected error while converting the file."
            job["progress"] = 0.0
        else:
            job["status"] = "completed"
            job["message"] = f"Finished. Saved to downloads/{Path(file_path).name}"
            job["progress"] = 100.0
            job["download_url"] = None
            job["file_path"] = str(file_path)


def _which(command: str) -> str | None:
    for folder in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(folder) / command
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)
