"""
Audio playback and streaming utilities.

This module provides audio playback functionality with real-time streaming
and signal emission for visualization purposes.
"""

import threading
import time
from dataclasses import dataclass
from typing import Any, Optional, Tuple

import numpy as np
import sounddevice as sd  # type: ignore
import soundfile as sf  # type: ignore
from PySide6 import QtCore

from config import AUDIO_CONFIG, ERROR_MESSAGES
from youtube_utils import download_youtube_to_wav, YouTubeDownloadError


@dataclass
class AudioSource:
    """
    Represents an audio source with its properties.
    
    Attributes:
        path: File path to the audio source
        samplerate: Sample rate in Hz
        channels: Number of audio channels
    """
    path: str
    samplerate: int
    channels: int


class AudioPlayerError(Exception):
    """Exception raised when audio playback fails."""


class AudioPlayer(QtCore.QObject):
    """
    Audio player with real-time streaming and visualization signal emission.
    
    This class reads frames from an audio file and feeds them to both a
    sounddevice OutputStream for playback and emits signals for visualization.
    It supports both local files and YouTube URLs.
    
    Signals:
        frame_available: Emitted with each audio chunk (np.ndarray) for visualization
        state_changed: Emitted when playback state changes (bool: playing or not)
    """
    
    # Qt signals for communication with GUI
    frame_available = QtCore.Signal(np.ndarray)  
    state_changed = QtCore.Signal(bool)

    def __init__(self, parent: Any = None) -> None:
        """
        Initialize the audio player.
        
        Args:
            parent: Optional parent QObject for Qt object hierarchy
        """
        super().__init__(parent)
        
        # Audio file and stream objects
        self._file: Optional[sf.SoundFile] = None
        self._stream: Optional[sd.OutputStream] = None
        
        # Threading control
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._paused = False
        self._lock = threading.Lock()
        
        # Audio configuration from config module
        self.blocksize = AUDIO_CONFIG["blocksize"]
        self.channels = AUDIO_CONFIG["default_channels"]
        self.samplerate = AUDIO_CONFIG["default_samplerate"]

    def open(self, path: str) -> Tuple[str, str]:
        """
        Open an audio source (local file or YouTube URL).
        
        Args:
            path: Path to audio file or YouTube URL
            
        Returns:
            Tuple of (actual_file_path, display_title)
            
        Raises:
            AudioPlayerError: If the audio source cannot be opened
            YouTubeDownloadError: If YouTube download fails
            
        Example:
            >>> player = AudioPlayer()
            >>> file_path, title = player.open("https://youtube.com/watch?v=...")
            >>> print(f"Opened: {title}")
        """
        title = ""
        actual_path = path
        
        try:
            # Handle YouTube URLs
            if self._is_youtube_url(path):
                actual_path, title = download_youtube_to_wav(path)
            
            # Open the audio file
            audio_file = sf.SoundFile(actual_path, mode='r')
            self._file = audio_file
            
            # Update audio parameters from file
            self.samplerate = audio_file.samplerate
            self.channels = audio_file.channels
            
            return actual_path, title
            
        except (OSError, sf.LibsndfileError) as e:
            raise AudioPlayerError(f"{ERROR_MESSAGES['audio_file_error']}: {str(e)}") from e
        except YouTubeDownloadError as e:
            # Re-raise YouTube errors without wrapping
            raise e

    def close(self) -> None:
        """
        Close the current audio source and stop playback.
        
        This method stops any active playback and releases all audio resources.
        """
        self.stop()
        if self._file is not None:
            self._file.close()
            self._file = None

    def play(self) -> None:
        """
        Start or resume audio playback.
        
        If audio is currently paused, this will resume playback.
        If no audio is playing, this will start playback from the current position.
        
        Raises:
            AudioPlayerError: If playback cannot be started
        """
        if self._file is None:
            return
            
        # If already running, just unpause
        if self._running:
            with self._lock:
                self._paused = False
            self.state_changed.emit(True)
            return
        
        # Start new playback thread
        self._running = True
        self._paused = False

        def audio_thread() -> None:
            """
            Main audio playback thread function.
            
            This function runs in a separate thread and handles the actual
            audio streaming and signal emission for visualization.
            """
            stream = None
            try:
                # Initialize audio stream with file parameters
                stream = sd.OutputStream(
                    samplerate=self.samplerate,
                    channels=self.channels,
                    blocksize=self.blocksize
                )
                self._stream = stream
                stream.start()
                
                while self._running:
                    # Check pause state
                    with self._lock:
                        paused = self._paused
                    
                    if paused:
                        time.sleep(0.02)  # Small sleep to prevent busy waiting
                        continue
                    
                    # Check for end of file
                    if self._file is not None and self._file.tell() >= len(self._file):
                        break  # Reached EOF
                    
                    # Read and play audio data
                    if self._file is not None:
                        data = self._file.read(self.blocksize, dtype='float32', always_2d=True)
                        
                        if len(data) == 0:
                            break  # No more data
                        
                        # Send to audio output
                        stream.write(data)
                        
                        # Emit signal for visualization (copy to avoid race conditions)
                        self.frame_available.emit(data.copy())
                        
            except Exception as e:
                # Log error but don't crash the application
                print(f"Audio thread error: {e}")
            finally:
                # Clean up audio stream
                if stream is not None:
                    try:
                        stream.stop()
                        stream.close()
                    except Exception:
                        pass  # Best effort cleanup
                
                self._stream = None
                self._running = False
                self.state_changed.emit(False)

        # Start the audio thread
        self._thread = threading.Thread(target=audio_thread, daemon=True)
        self._thread.start()
        self.state_changed.emit(True)

    def pause(self) -> None:
        """
        Pause audio playback.
        
        Playback can be resumed with play().
        """
        if not self._running:
            return
            
        with self._lock:
            self._paused = True
        self.state_changed.emit(False)

    def stop(self) -> None:
        """
        Stop audio playback completely.
        
        This stops the playback thread and releases audio resources.
        To resume, play() must be called again.
        """
        self._running = False
        
        # Wait for thread to finish
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        self._thread = None
        
        # Clean up stream
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass  # Best effort cleanup
            self._stream = None
    
    def reset(self) -> None:
        """
        Reset playback to the beginning of the audio file.
        
        If audio was playing, it will continue playing from the beginning.
        If audio was paused or stopped, it will remain in that state.
        """
        if self._file is None:
            return
            
        was_playing = self.is_running and not self.is_paused
        self.stop()
        
        # Reset file position to beginning
        self._file.seek(0)
        
        if was_playing:
            # Restart playback after a small delay for clean restart
            QtCore.QTimer.singleShot(50, self.play)

    @property
    def is_running(self) -> bool:
        """
        Check if audio playback is currently running.
        
        Returns:
            True if audio is playing or paused, False if stopped
        """
        return self._running
    
    @property
    def is_paused(self) -> bool:
        """
        Check if audio playback is currently paused.
        
        Returns:
            True if audio is paused, False if playing or stopped
        """
        return self._paused
    
    @property
    def position(self) -> int:
        """
        Get the current playback position in samples.
        
        Returns:
            Current position in the audio file (samples from start)
        """
        if self._file is not None:
            return int(self._file.tell())
        return 0
    
    @property
    def duration(self) -> int:
        """
        Get the total duration of the audio file in samples.
        
        Returns:
            Total length of the audio file in samples
        """
        if self._file is not None:
            return len(self._file)
        return 0
    
    def _is_youtube_url(self, url: str) -> bool:
        """
        Check if a URL appears to be a YouTube URL.
        
        Args:
            url: URL string to check
            
        Returns:
            True if URL looks like a YouTube URL, False otherwise
        """
        return url.lower().startswith('http') and 'youtube' in url.lower()