"""
YouTube audio download utilities.

This module handles downloading and converting YouTube videos to WAV format
for audio analysis in the goniometer application.
"""

import os
import tempfile
from typing import Tuple, Optional

import yt_dlp  # type: ignore

from config import YOUTUBE_CONFIG, FFMPEG_CONFIG, ERROR_MESSAGES


class YouTubeDownloadError(Exception):
    """Exception raised when YouTube download fails."""


class YouTubeDownloader:
    """
    Handles downloading audio from YouTube URLs.
    
    This class provides methods to download the best available audio stream
    from YouTube videos and convert them to WAV format for analysis.
    """
    
    def __init__(self, ffmpeg_path: Optional[str] = None):
        """
        Initialize the YouTube downloader.
        
        Args:
            ffmpeg_path: Optional custom FFmpeg installation path.
                        If None, uses the default Windows path from config.
        """
        self.ffmpeg_path = ffmpeg_path or FFMPEG_CONFIG["default_path"]
        
    def download_to_wav(self, url: str) -> Tuple[str, str]:
        """
        Download the best audio stream from YouTube and convert to WAV.
        
        Args:
            url: YouTube URL to download from
            
        Returns:
            Tuple of (wav_file_path, video_title)
            
        Raises:
            YouTubeDownloadError: If download or conversion fails
            FileNotFoundError: If the output WAV file is not created
            
        Example:
            >>> downloader = YouTubeDownloader()
            >>> wav_path, title = downloader.download_to_wav("https://youtube.com/watch?v=...")
            >>> print(f"Downloaded: {title}")
        """
        if not self._is_youtube_url(url):
            raise YouTubeDownloadError("URL does not appear to be a valid YouTube URL")
            
        # Create temporary directory for download
        tmpdir = tempfile.mkdtemp(prefix=YOUTUBE_CONFIG["temp_prefix"])
        wav_path = os.path.join(tmpdir, "audio.wav")
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': YOUTUBE_CONFIG["audio_format"],
            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'ffmpeg_location': self.ffmpeg_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': YOUTUBE_CONFIG["output_format"],
                'preferredquality': YOUTUBE_CONFIG["audio_quality"],
            }],
            'postprocessor_args': [
                '-ar', YOUTUBE_CONFIG["resample_rate"],  # Resample for consistency
                '-ac', YOUTUBE_CONFIG["channels"],       # Stereo output
            ],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info and download
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'YouTube Video')
                
                # Find the generated WAV file
                base = os.path.splitext(ydl.prepare_filename(info))[0]
                produced = base + '.wav'
                
                if not os.path.exists(produced):
                    raise FileNotFoundError(ERROR_MESSAGES["youtube_download_failed"])
                
                # Move to expected location
                os.replace(produced, wav_path)
                
        except yt_dlp.DownloadError as e:
            raise YouTubeDownloadError(f"yt-dlp download failed: {str(e)}") from e
        except Exception as e:
            raise YouTubeDownloadError(f"Unexpected error during download: {str(e)}") from e
            
        return wav_path, title
    
    def _is_youtube_url(self, url: str) -> bool:
        """
        Check if a URL appears to be a valid YouTube URL.
        
        Args:
            url: URL string to validate
            
        Returns:
            True if URL looks like a YouTube URL, False otherwise
        """
        youtube_domains = [
            'youtube.com',
            'www.youtube.com', 
            'youtu.be',
            'm.youtube.com',
            'music.youtube.com'
        ]
        
        url_lower = url.lower()
        return any(domain in url_lower for domain in youtube_domains)
    
    @staticmethod
    def validate_ffmpeg(ffmpeg_path: Optional[str] = None) -> bool:
        """
        Validate that FFmpeg is available at the specified path.
        
        Args:
            ffmpeg_path: Path to FFmpeg binary directory.
                        If None, uses default from config.
                        
        Returns:
            True if FFmpeg is found and executable, False otherwise
        """
        if ffmpeg_path is None:
            ffmpeg_path = str(FFMPEG_CONFIG["default_path"])
            
        ffmpeg_exe = os.path.join(ffmpeg_path, "ffmpeg.exe")
        return os.path.isfile(ffmpeg_exe) and os.access(ffmpeg_exe, os.X_OK)


def download_youtube_to_wav(url: str) -> Tuple[str, str]:
    """
    Convenience function to download YouTube audio to WAV format.
    
    This is a simple wrapper around YouTubeDownloader.download_to_wav()
    for backward compatibility with existing code.
    
    Args:
        url: YouTube URL to download
        
    Returns:
        Tuple of (wav_file_path, video_title)
        
    Raises:
        YouTubeDownloadError: If download fails
        FileNotFoundError: If FFmpeg is not found or output file is missing
    """
    downloader = YouTubeDownloader()
    
    # Validate FFmpeg availability
    if not YouTubeDownloader.validate_ffmpeg():
        raise FileNotFoundError(ERROR_MESSAGES["no_ffmpeg"])
    
    return downloader.download_to_wav(url)