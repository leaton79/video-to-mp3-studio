from __future__ import annotations

import re
from urllib.parse import urlparse
from urllib.parse import parse_qs


ALLOWED_BITRATES = ["128", "192", "256", "320"]
INVALID_FILENAME_CHARS = r'[<>:"/\\|?*\x00-\x1f]'


def validate_url(value: str) -> str | None:
    if not value:
        return "Enter a video URL."

    try:
        parsed = urlparse(value)
    except ValueError:
        return "Enter a valid URL."

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return "Enter a valid http or https URL."

    hostname = parsed.netloc.lower()
    if "youtube.com" in hostname or "youtu.be" in hostname:
        youtube_error = _validate_youtube_url(parsed)
        if youtube_error:
            return youtube_error

    return None


def _validate_youtube_url(parsed) -> str | None:
    video_id = None
    hostname = parsed.netloc.lower()

    if "youtu.be" in hostname:
        video_id = parsed.path.strip("/").split("/")[0]
    else:
        video_id = parse_qs(parsed.query).get("v", [""])[0]

    if not video_id:
        return "This YouTube link is missing the video ID."

    if not re.fullmatch(r"[\w-]{11}", video_id):
        return "This YouTube link looks incomplete. The video ID should be 11 characters."

    return None


def validate_filename(value: str) -> str | None:
    if not value:
        return "Enter an output file name."

    if len(value) > 120:
        return "Keep the file name under 120 characters."

    if re.search(INVALID_FILENAME_CHARS, value):
        return 'Do not use these characters: < > : " / \\ | ? *'

    if value.endswith("."):
        return "Do not end the file name with a period."

    return None
