"""Module for fetching YouTube video transcripts."""
import logging
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

            # Try to get English transcript directly
            try:
                logger.debug("Attempting to get English transcript...")
                return YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            except NoTranscriptFound:
                logger.debug("No English transcript found, trying alternatives...")
                # Try to get any transcript and translate to English
                transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
                logger.debug("Available transcripts:")
                for transcript in transcripts:
                    logger.debug(f"- {transcript.language_code}")

                # Get the first available transcript and translate it
                transcript = next(iter(transcripts))
                logger.debug(f"Translating from {transcript.language_code} to English...")
                return transcript.translate('en').fetch()

        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable,
                NoTranscriptAvailable, TranslationLanguageNotAvailable) as e:
            logger.error(f"Failed to fetch transcript: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise Exception(f"Failed to fetch transcript: {str(e)}")
