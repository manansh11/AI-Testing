"""Main module for the YouTube transcript tool."""
import sys
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
    args = parser.parse_args()

    # Validate URL
    if not URLParser.is_valid_url(args.url):
        print("Error: Invalid YouTube URL format.", file=sys.stderr)
        return 1

    # Extract video ID
    video_id = URLParser.extract_video_id(args.url)
    if not video_id:
        print("Error: Could not extract video ID from URL.", file=sys.stderr)
        return 1

    try:
        # Fetch transcript
        transcript_data = TranscriptFetcher.get_transcript(video_id)
        if not transcript_data:
            print("Error: No transcript data found.", file=sys.stderr)
            return 1

        # Format and print transcript
        formatted_transcript = OutputFormatter.format_transcript(transcript_data)
        print(formatted_transcript)
        return 0

    except TranscriptsDisabled:
        print("Error: Transcripts are disabled for this video.", file=sys.stderr)
        return 1
    except NoTranscriptFound:
        print("Error: No English transcript found for this video.", file=sys.stderr)
        return 1
    except VideoUnavailable:
        print("Error: The video is not available or requires authentication.", file=sys.stderr)
        return 1
    except NoTranscriptAvailable:
        print("Error: No transcripts are available for this video.", file=sys.stderr)
        return 1
    except TranslationLanguageNotAvailable:
        print("Error: English translation is not available for this video.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
