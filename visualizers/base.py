"""
Base Visualization Classes and Common Utilities.

This module provides the foundation classes and utilities for all audio
visualizers in the goniometer application. It defines the common interface
and shared functionality used by specialized visualizers.
"""

from abc import abstractmethod
from typing import Any

import numpy as np
import pyqtgraph as pg  # type: ignore


class BaseViz(pg.GraphicsLayoutWidget):  # type: ignore
    """
    Abstract base class for all audio visualizers.
    
    This class provides the common interface and basic setup for all
    visualizers. It inherits from pyqtgraph's GraphicsLayoutWidget to
    provide a high-performance plotting canvas.
    
    All concrete visualizers must implement the update_audio method
    to process incoming audio data and update their display.
    
    Attributes:
        samplerate (int): Audio sample rate in Hz
        
    Args:
        samplerate: Audio sample rate in Hz (e.g., 44100, 48000)
        parent: Optional parent widget for Qt hierarchy
        
    Example:
        >>> class MyVisualizer(BaseViz):
        ...     def update_audio(self, block):
        ...         # Process audio and update visualization
        ...         pass
        >>> viz = MyVisualizer(44100)
    """
    
    def __init__(self, samplerate: int, parent: Any = None) -> None:
        """
        Initialize the base visualizer.
        
        Sets up the graphics canvas with professional appearance
        suitable for audio analysis applications.
        
        Args:
            samplerate: Audio sample rate in Hz
            parent: Optional parent widget for Qt object hierarchy
        """
        super().__init__(parent)
        
        # Store audio parameters
        self.samplerate = samplerate
        
        # Configure appearance for professional audio analysis
        self.setBackground('k')  # Black background (standard for audio tools)
        self.setAntialiasing(True)  # Smooth rendering
        
        # Set up professional styling
        self._configure_appearance()
    
    def _configure_appearance(self) -> None:
        """
        Configure the visual appearance for professional audio analysis.
        
        This method sets up colors, fonts, and other visual elements
        to match industry-standard audio analysis tools.
        """
        # Configure default plot styling
        pg.setConfigOption('background', 'k')  # Black background
        pg.setConfigOption('foreground', 'w')  # White foreground
        pg.setConfigOption('antialias', True)  # Antialiasing
        
    @abstractmethod
    def update_audio(self, block: np.ndarray) -> None:
        """
        Process incoming audio data and update the visualization.
        
        This method must be implemented by all concrete visualizer classes.
        It receives real-time audio data and should update the visual
        display accordingly.
        
        Args:
            block: Audio data array with shape (samples, channels)
                  For mono: (samples,) or (samples, 1)
                  For stereo: (samples, 2)
                  Data type is typically float32 with values in [-1.0, 1.0]
                  
        Note:
            This method is called frequently (typically 30-60 times per second)
            so implementations should be efficient and avoid heavy computations.
            
        Example:
            >>> def update_audio(self, block):
            ...     if block.ndim == 2 and block.shape[1] == 2:
            ...         left, right = block[:, 0], block[:, 1]
            ...         # Update visualization with stereo data
            ...     else:
            ...         # Handle mono data
            ...         pass
        """
        raise NotImplementedError("Subclasses must implement update_audio method")
    
    def set_samplerate(self, samplerate: int) -> None:
        """
        Update the sample rate for the visualizer.
        
        This method should be called when the audio source changes
        and has a different sample rate.
        
        Args:
            samplerate: New sample rate in Hz
        """
        self.samplerate = samplerate
        
    def clear(self) -> None:
        """
        Clear the visualization display.
        
        This method clears all visual elements and resets the display.
        Useful when switching audio sources or stopping playback.
        """
        # Clear all plots in the layout
        self.clear()
        
    def reset(self) -> None:
        """
        Reset the visualizer to its initial state.
        
        This method resets any accumulated data or state in the visualizer
        while preserving the basic configuration.
        """
        self.clear()