from __future__ import annotations

import subprocess
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
    cookies_dir: Path,
    progress_callback: ProgressCallback,
) -> Path:
    if shutil.which("ffmpeg") is None:
        raise ToolMissingError(
            "FFmpeg is not installed. Install FFmpeg first, then try again."
        )

    yt_dlp_binary = _yt_dlp_binary()
    if yt_dlp_binary is None:
        raise ToolMissingError(
            "yt-dlp is not installed or not on your PATH. Install it first, then try again."
        )

    downloads_dir.mkdir(parents=True, exist_ok=True)
    final_path = downloads_dir / f"{output_name}.mp3"
    if final_path.exists():
        raise ConversionError("A file with that name already exists in the downloads folder.")

    try:
        progress_callback("running", "Contacting the video site...", 8.0)
        _download_with_cli(
            yt_dlp_binary=yt_dlp_binary,
            video_url=video_url,
            output_name=output_name,
            bitrate=bitrate,
            downloads_dir=downloads_dir,
            cookies_dir=cookies_dir,
            progress_callback=progress_callback,
        )
    except subprocess.CalledProcessError as exc:
        _cleanup_partial_files(downloads_dir, output_name)
        raise ConversionError(_friendly_download_error(exc)) from exc

    if not final_path.exists():
        matches = list(downloads_dir.glob(f"{output_name}*.mp3"))
        if not matches:
            raise ConversionError("Conversion finished, but the MP3 file was not found.")
        final_path = matches[0]

    progress_callback("completed", "Conversion complete.", 100.0)
    return final_path


def _download_with_cli(
    *,
    yt_dlp_binary: str,
    video_url: str,
    output_name: str,
    bitrate: str,
    downloads_dir: Path,
    cookies_dir: Path,
    progress_callback: ProgressCallback,
) -> None:
    output_template = str(downloads_dir / f"{output_name}.%(ext)s")
    base_command = [
        yt_dlp_binary,
        "--newline",
        "--progress",
        "--no-playlist",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        bitrate,
        "-o",
        output_template,
        video_url,
    ]
    cookies_file = cookies_dir / "youtube-cookies.txt"
    if _is_youtube_url(video_url) and cookies_file.exists():
        base_command = base_command[:1] + ["--cookies", str(cookies_file)] + base_command[1:]

    return_code, output = _run_command(base_command, progress_callback)
    if return_code == 0:
        return

    raise subprocess.CalledProcessError(
        returncode=return_code,
        cmd=base_command,
        output=output,
    )


def _run_command(command: list[str], progress_callback: ProgressCallback) -> tuple[int, str]:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    combined_output: list[str] = []
    assert process.stdout is not None

    for raw_line in process.stdout:
        line = raw_line.strip()
        if not line:
            continue
        combined_output.append(line)
        _handle_progress_line(line, progress_callback)

    return process.wait(), "\n".join(combined_output)


def _handle_progress_line(line: str, progress_callback: ProgressCallback) -> None:
    if line.startswith("[download]"):
        if "%" in line:
            percent = _extract_percent(line)
            if percent is not None:
                progress_callback("running", f"Downloading audio... {percent:.1f}%", percent * 0.7)
                return

        if "Destination:" in line:
            progress_callback("running", "Preparing download...", 18.0)
            return

        if "100%" in line:
            progress_callback("running", "Download finished. Converting to MP3...", 82.0)
            return

    if line.startswith("[ExtractAudio]"):
        progress_callback("running", "Converting audio to MP3...", 94.0)
        return

    if line.startswith("[youtube]") or line.startswith("[youtube:tab]"):
        progress_callback("running", "Contacting YouTube...", 12.0)


def _extract_percent(line: str) -> float | None:
    for chunk in line.split():
        if chunk.endswith("%"):
            try:
                return float(chunk[:-1])
            except ValueError:
                return None
    return None


def _is_youtube_url(url: str) -> bool:
    return "youtube.com/" in url or "youtu.be/" in url


def _yt_dlp_binary() -> str | None:
    preferred_paths = [
        "/opt/homebrew/bin/yt-dlp",
        shutil.which("yt-dlp"),
    ]
    for candidate in preferred_paths:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def _cleanup_partial_files(downloads_dir: Path, output_name: str) -> None:
    for pattern in (f"{output_name}*.part", f"{output_name}*.ytdl"):
        for path in downloads_dir.glob(pattern):
            try:
                path.unlink()
            except OSError:
                pass


def _friendly_download_error(error: Exception) -> str:
    message = getattr(error, "output", "") or str(error)
    message = message.strip()
    if "ERROR:" in message:
        message = message.split("ERROR:", 1)[1].strip()

    if "Video unavailable" in message:
        return "Video unavailable. Double-check the video link. For YouTube, the video ID must be exactly 11 characters."

    if "HTTP Error 403: Forbidden" in message:
        return "Download blocked by the video site (HTTP 403). For YouTube, add a cookies file at cookies/youtube-cookies.txt and try again."

    if message:
        return f"Download failed: {message}"

    return "Download failed. Check the URL, confirm the site is supported, and try again."
