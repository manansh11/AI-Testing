"""Setup configuration for the YouTube transcript tool."""
from setuptools import setup, find_packages

setup(
    name="youtube-transcript-tool",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "youtube-transcript-api>=0.6.0",
        "pytube>=15.0.0",
    ],
    entry_points={
        "console_scripts": [
            "youtube-transcript=youtube_transcript_tool.__main__:main",
        ],
    },
    python_requires=">=3.8",
)
