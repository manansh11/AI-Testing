"""Module for fetching YouTube video transcripts."""
from typing import Optional, Dict, Any
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api._errors import NoTranscriptFound


class TranscriptFetcher:
    """Class responsible for fetching and processing YouTube transcripts."""

    @staticmethod
    def get_transcript(video_id: str) -> Optional[str]:
        """
        Fetch the English transcript for a YouTube video.

        Args:
            video_id (str): The YouTube video ID.

        Returns:
            Optional[str]: The transcript text if found, None otherwise.

        Raises:
            TranscriptsDisabled: If transcripts are disabled for the video.
            NoTranscriptFound: If no English transcript is available.
        """
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript(['en'])
            return transcript.fetch()
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to fetch transcript: {str(e)}")
