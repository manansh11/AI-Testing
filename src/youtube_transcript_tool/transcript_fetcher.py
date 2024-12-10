"""Module for fetching YouTube video transcripts."""
import logging
from typing import Optional, Dict, Any, List
from pytube import YouTube
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

            # Try pytube first
            try:
                logger.debug("Attempting to fetch transcript using pytube...")
                url = f"https://www.youtube.com/watch?v={video_id}"
                yt = YouTube(url)

                captions = yt.captions
                logger.debug(f"Available caption tracks: {list(captions.keys()) if captions else 'None'}")

                if not captions:
                    logger.debug("No captions found in pytube")
                    raise NoTranscriptAvailable()

                # Try English variants
                english_codes = ['en', 'a.en', 'en-GB', 'en-US']
                caption = None
                for code in english_codes:
                    if code in captions:
                        caption = captions[code]
                        break

                if caption:
                    logger.debug(f"Found English caption track: {caption.code}")
                    caption_xml = caption.xml_captions
                    # Parse the XML captions into our format
                    from xml.etree import ElementTree
                    root = ElementTree.fromstring(caption_xml)
                    transcript = []
                    for text in root.findall('.//text'):
                        start = float(text.get('start', 0))
                        duration = float(text.get('dur', 0))
                        content = text.text.strip() if text.text else ""
                        if content:
                            transcript.append({
                                "text": content,
                                "start": start,
                                "duration": duration
                            })
                    return transcript

            except Exception as pytube_error:
                logger.debug(f"Pytube attempt failed: {str(pytube_error)}")
                # Fall back to youtube-transcript-api
                logger.debug("Falling back to youtube-transcript-api...")
                try:
                    return YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                except NoTranscriptFound:
                    # Try to get any transcript and translate to English
                    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
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
