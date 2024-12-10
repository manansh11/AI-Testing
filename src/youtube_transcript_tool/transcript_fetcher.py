"""Module for fetching YouTube video transcripts."""
import logging
import requests
from typing import Optional, Dict, Any, List
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    VideoUnavailable,
    NoTranscriptAvailable,
    TranslationLanguageNotAvailable,
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TranscriptFetcher:
    """Class responsible for fetching and processing YouTube transcripts."""

    @staticmethod
    def _get_cookies(video_id: str) -> Dict[str, str]:
        """
        Get necessary cookies for accessing YouTube content.

        Args:
            video_id (str): The YouTube video ID.

        Returns:
            Dict[str, str]: Dictionary of cookies.
        """
        try:
            # Make a request to the video page to get cookies
            url = f"https://www.youtube.com/watch?v={video_id}"
            response = requests.get(url)
            return response.cookies.get_dict()
        except Exception as e:
            logger.warning(f"Failed to get cookies: {str(e)}")
            return {}

    @staticmethod
    def get_transcript(video_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch the English transcript for a YouTube video.

        Args:
            video_id (str): The YouTube video ID.

        Returns:
            Optional[List[Dict[str, Any]]]: List of transcript entries if found, None otherwise.

        Raises:
            TranscriptsDisabled: If transcripts are disabled for the video.
            NoTranscriptFound: If no English transcript is available.
            VideoUnavailable: If the video is not accessible.
            NoTranscriptAvailable: If no transcripts are available.
            TranslationLanguageNotAvailable: If English translation is not available.
        """
        try:
            logger.debug(f"Attempting to fetch transcripts for video ID: {video_id}")

            # Get cookies for authentication
            cookies = TranscriptFetcher._get_cookies(video_id)
            logger.debug("Retrieved cookies for authentication")

            # First, list available transcripts
            logger.debug("Listing available transcripts...")
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, cookies=cookies)

            logger.debug("Available transcripts:")
            for transcript in transcript_list:
                logger.debug(f"- {transcript.language_code}")

            # Try to get English transcript directly
            try:
                logger.debug("Attempting to find English transcript...")
                transcript = transcript_list.find_transcript(['en'])
                logger.debug("Found English transcript, fetching...")
                return transcript.fetch()
            except NoTranscriptFound:
                logger.debug("No direct English transcript found, trying alternatives...")
                # Try US/GB English variants
                try:
                    transcript = transcript_list.find_transcript(['en-US', 'en-GB'])
                    logger.debug("Found US/GB English variant, fetching...")
                    return transcript.fetch()
                except NoTranscriptFound:
                    # Get the first available transcript and translate it
                    logger.debug("No English variants found, attempting translation...")
                    transcript = next(iter(transcript_list))
                    logger.debug(f"Translating from {transcript.language_code} to English...")
                    return transcript.translate('en').fetch()

        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable,
                NoTranscriptAvailable, TranslationLanguageNotAvailable) as e:
            logger.error(f"Failed to fetch transcript: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise Exception(f"Failed to fetch transcript: {str(e)}")
