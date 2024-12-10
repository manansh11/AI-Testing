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

            # First, try to list all available transcripts
            try:
                logger.debug("Listing all available transcripts...")
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

                logger.debug("Available transcripts:")
                available_languages = []
                for transcript in transcript_list:
                    available_languages.append(transcript.language_code)
                    logger.debug(f"- {transcript.language_code}")

                if not available_languages:
                    logger.error("No transcripts available for this video")
                    raise NoTranscriptAvailable()

                # Try English variants first
                english_variants = ['en', 'en-US', 'en-GB']
                for lang in english_variants:
                    if lang in available_languages:
                        logger.debug(f"Found {lang} transcript, fetching...")
                        return YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])

                # If no English transcript, get the first available and translate
                logger.debug("No English transcript found, using first available transcript...")
                first_transcript = transcript_list.find_transcript(available_languages)
                logger.debug(f"Translating from {first_transcript.language_code} to English...")
                return first_transcript.translate('en').fetch()

            except Exception as e:
                logger.debug(f"Error listing transcripts: {str(e)}")
                # Fallback: try direct transcript retrieval
                logger.debug("Attempting direct transcript retrieval...")
                return YouTubeTranscriptApi.get_transcript(
                    video_id,
                    languages=['en', 'en-US', 'en-GB'],
                    continue_after_error=True
                )

        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable,
                NoTranscriptAvailable, TranslationLanguageNotAvailable) as e:
            logger.error(f"Failed to fetch transcript: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise Exception(f"Failed to fetch transcript: {str(e)}")
