# YouTube Transcript Tool - Product Requirements Document

## Purpose and Scope
### Goal
Create a command-line tool that fetches English transcripts from YouTube videos using only the video URL.

### Scope
- Support publicly available YouTube videos with transcripts
- No authentication or API keys required
- Focus on English transcripts only
- Command-line interface only

### Out of Scope
- Videos without transcripts
- Private or age-restricted videos
- Non-English transcripts
- GUI interface
- Transcript editing capabilities

## System Architecture

### Components
1. Input Parser
   - Validates YouTube URL format
   - Extracts video ID from URL
   - Handles various YouTube URL formats (full, shortened, embedded)

2. Transcript Fetcher
   - Makes HTTP requests to YouTube
   - Retrieves available transcripts
   - Selects English transcript if available
   - Processes raw transcript data

3. Output Formatter
   - Cleans transcript text
   - Formats output for readability
   - Handles stdout writing

### Data Flow
1. User inputs YouTube URL via command line
2. System validates URL and extracts video ID
3. System fetches available transcripts
4. System processes and formats English transcript
5. System outputs formatted transcript to stdout

### External Dependencies
- `youtube-transcript-api`: Primary library for fetching transcripts
- Python 3.x runtime environment
- Network connectivity
- Standard Python libraries (re, sys, argparse)

## Feature Requirements

### Core Features
1. URL Validation
   - Accept and validate YouTube URL input
   - Support various YouTube URL formats
   - Provide clear error messages for invalid URLs

2. Transcript Retrieval
   - Fetch available transcripts
   - Select English transcript
   - Handle missing transcript scenarios
   - Support timeout and retry mechanisms

3. Output Formatting
   - Clean text formatting
   - Proper spacing and line breaks
   - Human-readable output
   - Clear error messages

### Acceptance Criteria
- Tool accepts valid YouTube URL and returns transcript
- Tool handles invalid URLs with appropriate error messages
- Tool handles missing transcripts gracefully
- Output is clean and readable
- Performance is acceptable (< 5s for most videos)

## Testing Strategy

### Unit Tests
1. URL Validation Tests
   - Test various URL formats
   - Test invalid URLs
   - Test edge cases (empty string, non-YouTube URLs)

2. Transcript Processing Tests
   - Test transcript cleaning
   - Test formatting functions
   - Test error handling

### Integration Tests
1. Basic Functionality
   - Test with short video (< 1 minute)
   - Test with medium video (5-10 minutes)
   - Test with long video (> 30 minutes)

2. Error Handling
   - Test with private videos
   - Test with videos without transcripts
   - Test with network issues

### Test Cases
1. Happy Path
   - Known video with English transcript
   - Various URL formats
   - Different video lengths

2. Error Cases
   - Invalid URLs
   - Missing transcripts
   - Network timeout
   - Non-English only videos

## Build Instructions

### Setup
1. Create Python virtual environment
2. Install required dependencies:
   ```bash
   pip install youtube-transcript-api
   ```

### Development
1. Follow PEP 8 style guide
2. Use type hints
3. Include docstrings for all functions
4. Keep functions focused and small

### Code Style Guidelines
- Follow PEP 8 conventions
- Use meaningful variable names
- Include type hints
- Write comprehensive docstrings
- Keep functions under 20 lines
- Use consistent naming conventions

## Troubleshooting Guide

### Common Issues
1. Network Connectivity
   - Check internet connection
   - Verify YouTube accessibility
   - Check for rate limiting

2. URL Issues
   - Verify URL format
   - Check video accessibility
   - Verify video has captions

3. Transcript Issues
   - Check for available transcripts
   - Verify English transcript exists
   - Check for format changes

### Support Steps
1. Network Issues
   - Run network connectivity test
   - Check YouTube API status
   - Verify proxy settings if applicable

2. URL Problems
   - Validate URL format
   - Test video accessibility in browser
   - Check video permissions

3. Transcript Errors
   - Verify transcript availability
   - Check for API changes
   - Review error messages

## Version Control
- GitHub repository: https://github.com/manansh11/AI-Testing
- Branch naming: feature/, bugfix/, hotfix/
- Commit messages: Follow conventional commits

## Future Enhancements (Out of Current Scope)
- Support for multiple languages
- GUI interface
- Transcript download in various formats
- Batch processing of multiple URLs
- Authentication support for private videos
