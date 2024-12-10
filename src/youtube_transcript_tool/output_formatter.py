"""Module for formatting transcript output."""
from typing import List, Dict, Any


class OutputFormatter:
    """Class responsible for formatting transcript output."""

    @staticmethod
    def format_transcript(transcript_data: List[Dict[str, Any]]) -> str:
        """
        Format the transcript data into readable text.

        Args:
            transcript_data (List[Dict[str, Any]]): List of transcript segments.

        Returns:
            str: Formatted transcript text.
        """
        formatted_lines = []
        for entry in transcript_data:
            text = entry.get('text', '').strip()
            if text:
                formatted_lines.append(text)

        return '\n'.join(formatted_lines)
