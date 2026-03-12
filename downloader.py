from __future__ import annotations

import shutil
from pathlib import Path
from typing import Callable


class ToolMissingError(RuntimeError):
    pass


class ConversionError(RuntimeError):
    pass


ProgressCallback = Callable[[str, str, float | None], None]


def start_conversion(
    *,
    video_url: str,
    output_name: str,
    bitrate: str,
    downloads_dir: Path,
    progress_callback: ProgressCallback,
) -> Path:
    if shutil.which("ffmpeg") is None:
        raise ToolMissingError(
            "FFmpeg is not installed. Install FFmpeg first, then try again."
        )

    if shutil.which("yt-dlp") is None:
        raise ToolMissingError(
            "yt-dlp is not installed or not on your PATH. Install it first, then try again."
        )

    try:
        from yt_dlp import YoutubeDL
        from yt_dlp.utils import DownloadError
    except ImportError as exc:
        raise ToolMissingError(
            "The Python yt-dlp package is not installed. Run pip install -r requirements.txt first."
        ) from exc

    downloads_dir.mkdir(parents=True, exist_ok=True)
    final_path = downloads_dir / f"{output_name}.mp3"
    if final_path.exists():
        raise ConversionError("A file with that name already exists in the downloads folder.")

    temp_template = str(downloads_dir / f"{output_name}.%(ext)s")

    def hook(data: dict) -> None:
        status = data.get("status")
        if status == "downloading":
            percent_text = data.get("_percent_str", "0%").strip().replace("%", "")
            try:
                percent = float(percent_text)
            except ValueError:
                percent = 25.0
            progress_callback("running", f"Downloading audio... {percent:.1f}%", percent * 0.7)
        elif status == "finished":
            progress_callback("running", "Download finished. Converting to MP3...", 82.0)

    ydl_options = {
        "format": "bestaudio/best",
        "outtmpl": temp_template,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [hook],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": bitrate,
            }
        ],
        "postprocessor_hooks": [_postprocessor_hook(progress_callback)],
    }

    try:
        progress_callback("running", "Contacting the video site...", 8.0)
        with YoutubeDL(ydl_options) as ydl:
            ydl.download([video_url])
    except DownloadError as exc:
        raise ConversionError(
            "Download failed. Check the URL, confirm the site is supported, and try again."
        ) from exc

    if not final_path.exists():
        matches = list(downloads_dir.glob(f"{output_name}*.mp3"))
        if not matches:
            raise ConversionError("Conversion finished, but the MP3 file was not found.")
        final_path = matches[0]

    progress_callback("completed", "Conversion complete.", 100.0)
    return final_path


def _postprocessor_hook(progress_callback: ProgressCallback):
    def hook(data: dict) -> None:
        status = data.get("status")
        if status == "started":
            progress_callback("running", "Preparing MP3 conversion...", 88.0)
        elif status == "processing":
            progress_callback("running", "Converting audio to MP3...", 94.0)
        elif status == "finished":
            progress_callback("running", "Finalizing your file...", 98.0)

    return hook
