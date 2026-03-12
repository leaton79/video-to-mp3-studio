from __future__ import annotations

import re
from urllib.parse import urlparse


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
