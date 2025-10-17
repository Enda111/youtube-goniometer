"""
Audio Visualizer Package for Professional Goniometer Analysis.

This package provides specialized audio visualization components designed
for professional audio analysis, with focus on stereo field visualization
and phase correlation analysis.

Components:
    BaseViz: Abstract base class for all visualizers
    GonioViz: Professional goniometer for stereo field analysis

Theory:
    A goniometer (from Greek 'gonia' meaning angle) is a professional
    audio tool that displays the relationship between left and right
    channels in stereo audio. It plots left channel amplitude on the
    X-axis and right channel amplitude on the Y-axis, creating patterns
    that reveal:
    
    - Stereo width and imaging
    - Phase relationships between channels  
    - Mono compatibility issues
    - Channel correlation
    
    Visual Interpretation:
    - Center point (0,0): Perfect mono signal
    - Horizontal line: Only left channel active
    - Vertical line: Only right channel active
    - Diagonal line (L=R): Mono signal in stereo
    - Anti-diagonal (L=-R): Out-of-phase stereo
    - Circular patterns: Uncorrelated stereo content
    - Elliptical patterns: Correlated stereo with width

Usage:
    >>> from visualizers import GonioViz
    >>> gonio = GonioViz(samplerate=44100)
    >>> gonio.update_audio(stereo_audio_data)
"""

from .base import BaseViz
from .gonio import GonioViz

__version__ = "1.0.0"
__author__ = "Audio Visualizer Team"

__all__ = [
    'BaseViz',
    'GonioViz',
]