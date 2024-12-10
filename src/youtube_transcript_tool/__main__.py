"""Main module for the YouTube transcript tool."""
import sys
import logging
import argparse
from .url_parser import URLParser
from .transcript_fetcher import TranscriptFetcher
from .output_formatter import OutputFormatter
from youtube_transcript_api import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    NoTranscriptAvailable,
    TranslationLanguageNotAvailable,
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main() -> int:
    """
    Main entry point for the YouTube transcript tool.

    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        description='Fetch English transcript from a YouTube video.'
    )
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    logger.debug(f"Processing URL: {args.url}")

    # Validate URL
    if not URLParser.is_valid_url(args.url):
        logger.error("Invalid YouTube URL format")
        print("Error: Invalid YouTube URL format.", file=sys.stderr)
        return 1

    # Extract video ID
    video_id = URLParser.extract_video_id(args.url)
    if not video_id:
        logger.error("Could not extract video ID from URL")
        print("Error: Could not extract video ID from URL.", file=sys.stderr)
        return 1

    logger.debug(f"Extracted video ID: {video_id}")

    try:
        # Fetch transcript
        logger.debug("Attempting to fetch transcript...")
        transcript_data = TranscriptFetcher.get_transcript(video_id)
        if not transcript_data:
            logger.error("No transcript data found")
            print("Error: No transcript data found.", file=sys.stderr)
            return 1

        # Format and print transcript
        logger.debug("Formatting transcript...")
        formatted_transcript = OutputFormatter.format_transcript(transcript_data)
        print(formatted_transcript)
        return 0

    except TranscriptsDisabled:
        logger.error("Transcripts are disabled for this video")
        print("Error: Transcripts are disabled for this video.", file=sys.stderr)
        return 1
    except NoTranscriptFound:
        logger.error("No English transcript found for this video")
        print("Error: No English transcript found for this video.", file=sys.stderr)
        return 1
    except VideoUnavailable:
        logger.error("The video is not available or requires authentication")
        print("Error: The video is not available or requires authentication.", file=sys.stderr)
        return 1
    except NoTranscriptAvailable:
        logger.error("No transcripts are available for this video")
        print("Error: No transcripts are available for this video.", file=sys.stderr)
        return 1
    except TranslationLanguageNotAvailable:
        logger.error("English translation is not available for this video")
        print("Error: English translation is not available for this video.", file=sys.stderr)
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
