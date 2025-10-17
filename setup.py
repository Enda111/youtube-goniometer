#!/usr/bin/env python3
"""
Setup script for YouTube Goniometer.

This file provides backward compatibility for systems that don't support
pyproject.toml. The primary build configuration is in pyproject.toml.
"""

from setuptools import setup, find_packages  # type: ignore
import os

# Read README for long description
def read_readme() -> str:
    """Read README.md for the long description."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Professional goniometer for YouTube audio analysis"

setup(
    name="youtube-goniometer",
    version="1.0.0",
    author="Audio Visualizer Team",
    author_email="contact@example.com",
    description="Professional goniometer for YouTube audio analysis with real-time stereo field visualization",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/youtube-goniometer",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/youtube-goniometer/issues",
        "Documentation": "https://github.com/yourusername/youtube-goniometer/blob/main/README.md",
        "Source Code": "https://github.com/yourusername/youtube-goniometer",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers", 
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "sounddevice>=0.4.4", 
        "soundfile>=0.10.0",
        "PySide6>=6.2.0",
        "pyqtgraph>=0.12.0",
        "yt-dlp>=2023.1.6",
    ],
    extras_require={
        "dev": [
            "black>=22.0.0",
            "pylint>=2.12.0",
            "mypy>=0.910",
            "pytest>=6.0.0",
            "pytest-qt>=4.0.0",
            "pytest-cov>=3.0.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "sphinx-autodoc-typehints>=1.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "youtube-goniometer=app:main",
            "goniometer=app:main",
        ],
        "gui_scripts": [
            "youtube-goniometer-gui=app:main",
        ],
    },
    keywords=[
        "audio", "goniometer", "stereo", "visualization", "youtube",
        "phase-correlation", "broadcast", "mastering", "music-production"
    ],
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yaml", "*.yml"],
    },
    zip_safe=False,
)