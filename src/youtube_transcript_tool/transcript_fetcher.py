"""Module for fetching YouTube video transcripts."""
from typing import Optional, Dict, Any, List
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    VideoUnavailable,
    NoTranscriptAvailable,
    TranslationLanguageNotAvailable,
)


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
            # First, list available transcripts
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Try to get English transcript directly
            try:
                transcript = transcript_list.find_transcript(['en'])
                return transcript.fetch()
            except NoTranscriptFound:
                # If no English transcript, try to get any transcript and translate to English
                transcript = transcript_list.find_transcript(['en-US', 'en-GB'])
                if not transcript:
                    # Get the first available transcript and translate it
                    transcript = next(iter(transcript_list))
                return transcript.translate('en').fetch()

        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable,
                NoTranscriptAvailable, TranslationLanguageNotAvailable) as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to fetch transcript: {str(e)}")
