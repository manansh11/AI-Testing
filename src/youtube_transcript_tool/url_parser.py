"""Module for parsing and validating YouTube URLs."""
from typing import Optional
import re


class URLParser:
    """Class responsible for parsing and validating YouTube URLs."""

    # Common YouTube URL patterns
    URL_PATTERNS = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]+)'
    ]

    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract the video ID from a YouTube URL.

        Args:
            url (str): The YouTube URL to parse.

        Returns:
            Optional[str]: The video ID if found, None otherwise.
        """
        if not url:
            return None

        for pattern in URLParser.URL_PATTERNS:
            match = re.match(pattern, url)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Check if the provided URL is a valid YouTube URL.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        return any(re.match(pattern, url) for pattern in URLParser.URL_PATTERNS)
