"""
Professional Goniometer Visualization for Stereo Audio Analysis.

This module implements a professional-grade goniometer (also known as a 
vector scope or correlation meter) used in audio engineering and mastering.
The goniometer provides real-time visualization of stereo field relationships
and phase correlation between left and right channels.

Technical Background:
    A goniometer plots left channel amplitude on the X-axis and right channel
    amplitude on the Y-axis. This creates visual patterns that reveal:
    
    - Stereo width and imaging characteristics
    - Phase relationships between channels
    - Mono compatibility issues
    - Channel balance and correlation
    - Out-of-phase content detection
    
Visual Pattern Interpretation:
    - Center point (0,0): Perfect mono signal
    - Horizontal line: Only left channel active  
    - Vertical line: Only right channel active
    - 45° diagonal (L=R): Mono signal in both channels
    - -45° diagonal (L=-R): Anti-phase stereo (mono incompatible)
    - Circular patterns: Uncorrelated stereo content (wide stereo)
    - Elliptical patterns: Correlated stereo with controllable width
    - Tight cluster: Narrow stereo image
    - Wide spread: Wide stereo image

Phase Correlation Values:
    +1.0: Perfect positive correlation (mono)
    +0.8 to +1.0: Good stereo correlation
    +0.3 to +0.8: Moderate correlation
    0.0: Uncorrelated (maximum stereo width)
    -0.3 to 0.0: Some anti-correlation
    -1.0: Perfect anti-correlation (mono incompatible)
"""

from typing import Any, List
import numpy as np
import pyqtgraph as pg  # type: ignore
from PySide6 import QtCore

from .base import BaseViz
from config import COLORS, GONIOMETER_CONFIG, PHASE_THRESHOLDS


class GonioViz(BaseViz):
    """
    Professional Goniometer for Real-Time Stereo Field Analysis.
    
    This visualizer implements a broadcast-quality goniometer that displays
    the relationship between left and right audio channels in real-time.
    It includes phase correlation analysis, trail effects, and professional
    reference lines commonly found in high-end audio equipment.
    
    Features:
        - Real-time L/R channel correlation display
        - Phase correlation coefficient calculation and display
        - Visual trail effects showing recent audio history
        - Professional reference lines for mono and anti-phase detection
        - Color-coded phase correlation indicators
        - Broadcast-standard visual appearance
        
    Args:
        samplerate: Audio sample rate in Hz
        parent: Optional parent widget
        
    Example:
        >>> gonio = GonioViz(44100)
        >>> # In audio callback:
        >>> gonio.update_audio(stereo_audio_block)
    """
    
    def __init__(self, samplerate: int, parent: Any = None) -> None:
        """
        Initialize the professional goniometer display.
        
        Sets up the plotting area, reference lines, trail effects,
        and phase correlation display according to broadcast standards.
        """
        super().__init__(samplerate, parent)
        
        # Create main plot with professional appearance
        self.plot = self.addPlot(title='Goniometer - Stereo Field Analysis')
        self._setup_plot_appearance()
        self._create_reference_lines()
        self._setup_visualization_elements()
        self._setup_phase_correlation_display()
        
        # Audio processing parameters from configuration
        self.max_points = int(GONIOMETER_CONFIG["max_points"])
        self.normalization_alpha = 0.8  # For peak normalization smoothing
        
        # Trail effect data storage
        self.trail_data: List[np.ndarray] = []
        self.trail_max_frames = int(GONIOMETER_CONFIG["trail_max_frames"])
        
    def _setup_plot_appearance(self) -> None:
        """Configure the plot appearance to professional standards."""
        plot_range = GONIOMETER_CONFIG["plot_range"]
        
        # Lock aspect ratio for accurate geometric interpretation
        self.plot.setAspectLocked(GONIOMETER_CONFIG["aspect_locked"])
        
        # Set measurement range (typically ±1.0 for normalized audio)
        self.plot.setRange(xRange=plot_range, yRange=plot_range)
        
        # Enable professional grid for precise measurement
        self.plot.showGrid(
            x=GONIOMETER_CONFIG["show_grid"], 
            y=GONIOMETER_CONFIG["show_grid"], 
            alpha=GONIOMETER_CONFIG["grid_alpha"]
        )
        
        # Set axis labels following broadcast conventions
        self.plot.setLabel('left', 'Right Channel (R)')
        self.plot.setLabel('bottom', 'Left Channel (L)')
        
        # Professional dark background
        self.setBackground(COLORS["plot_bg"])
        
    def _create_reference_lines(self) -> None:
        """
        Create professional reference lines for audio analysis.
        
        These lines help engineers quickly identify:
        - Mono content (diagonal lines)
        - Channel balance (center cross)
        - Phase relationships
        """
        center_color = COLORS["center_lines"]
        diag_color = COLORS["diagonal_lines"]
        
        # Center cross lines (L=0, R=0) - show channel balance
        center_line_width = int(GONIOMETER_CONFIG["line_widths"]["center"])
        center_line_style = str(GONIOMETER_CONFIG["center_line_style"]).title() + "Line"
        center_pen = pg.mkPen(
            center_color, 
            width=center_line_width,
            style=getattr(QtCore.Qt.PenStyle, center_line_style)
        )
        
        plot_range = GONIOMETER_CONFIG["plot_range"]
        self.plot.plot([0, 0], plot_range, pen=center_pen)  # Vertical (R=0)
        self.plot.plot(plot_range, [0, 0], pen=center_pen)  # Horizontal (L=0)
        
        # Diagonal reference lines for mono detection
        diag_line_width = int(GONIOMETER_CONFIG["line_widths"]["diagonal"])
        diag_line_style = str(GONIOMETER_CONFIG["diagonal_line_style"]).title() + "Line"
        diag_pen = pg.mkPen(
            diag_color,
            width=diag_line_width, 
            style=getattr(QtCore.Qt.PenStyle, diag_line_style)
        )
        
        # L=R diagonal (mono in both channels)
        self.plot.plot([-1, 1], [-1, 1], pen=diag_pen)
        
        # L=-R diagonal (anti-phase mono - mono incompatible!)  
        self.plot.plot([-1, 1], [1, -1], pen=diag_pen)
        
    def _setup_visualization_elements(self) -> None:
        """Setup the main visualization elements (scatter plot and trails)."""
        # Main scatter plot for current audio samples
        scatter_color = COLORS["scatter_main"]
        self.scatter = pg.ScatterPlotItem(
            size=GONIOMETER_CONFIG["scatter_size"],
            brush=pg.mkBrush(scatter_color),
            pen=None  # No outline for performance
        )
        self.plot.addItem(self.scatter)
        
        # Trail effect curves for visual persistence
        self.trail_curves = []
        trail_colors = COLORS["trail_colors"]
        
        trail_line_width = int(GONIOMETER_CONFIG["line_widths"]["trail"])
        for color in trail_colors:
            trail_pen = pg.mkPen(
                color, 
                width=trail_line_width
            )
            curve = self.plot.plot(pen=trail_pen)
            self.trail_curves.append(curve)
            
    def _setup_phase_correlation_display(self) -> None:
        """Setup the phase correlation coefficient display."""
        self.phase_text = pg.TextItem(
            text='Phase: --', 
            color=COLORS["text_primary"],
            anchor=(0, 1)  # Top-left anchor
        )
        self.plot.addItem(self.phase_text)
        
        # Position in top-left corner of plot
        plot_range = GONIOMETER_CONFIG["plot_range"]
        range_min, range_max = float(plot_range[0]), float(plot_range[1])
        self.phase_text.setPos(range_min * 0.9, range_max * 0.9)
        
    def update_audio(self, block: np.ndarray) -> None:
        """
        Update the goniometer display with new audio data.
        
        This method processes incoming stereo audio data and updates
        the visualization including scatter plot, trail effects, and
        phase correlation analysis.
        
        Args:
            block: Audio data with shape (samples,) for mono or 
                  (samples, 2) for stereo. Values should be in 
                  range [-1.0, 1.0] for proper visualization.
                  
        Processing Steps:
            1. Extract left and right channels
            2. Downsample if necessary for performance
            3. Normalize for consistent display range
            4. Calculate phase correlation coefficient
            5. Update scatter plot and trail effects
        """
        # Extract stereo channels
        left, right = self._extract_channels(block)
        
        # Downsample for performance if needed
        left, right = self._downsample_if_needed(left, right)
        
        # Normalize for display (prevents clipping visualization)
        left, right = self._normalize_channels(left, right)
        
        # Calculate and display phase correlation
        self._update_phase_correlation(left, right)
        
        # Update main visualization
        self._update_scatter_plot(left, right)
        
        # Update trail effect
        self._update_trail_effect(left, right)
        
    def _extract_channels(self, block: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Extract left and right channels from audio block.
        
        Args:
            block: Audio data array
            
        Returns:
            Tuple of (left_channel, right_channel) arrays
        """
        if block.ndim == 1:
            # Mono input - create pseudo-stereo for visualization
            left = block
            right = block * 0.8  # Slight attenuation to show stereo effect
        else:
            # Stereo input
            left = block[:, 0]
            right = block[:, 1] if block.shape[1] > 1 else block[:, 0]
            
        return left, right
        
    def _downsample_if_needed(self, left: np.ndarray, right: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Downsample audio data if it exceeds display point limit.
        
        Args:
            left: Left channel data
            right: Right channel data
            
        Returns:
            Downsampled (left, right) tuple
        """
        if len(left) > self.max_points:
            # Use integer decimation for even sampling
            step = len(left) // self.max_points
            left = left[::step]
            right = right[::step]
            
        return left, right
        
    def _normalize_channels(self, left: np.ndarray, right: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Normalize channels for consistent goniometer display.
        
        Uses peak normalization to ensure full use of display range
        while maintaining relative channel relationships.
        
        Args:
            left: Left channel data
            right: Right channel data
            
        Returns:
            Normalized (left, right) tuple
        """
        if len(left) == 0:
            return left, right
            
        # Find peak levels for normalization
        left_peak = np.max(np.abs(left))
        right_peak = np.max(np.abs(right))
        overall_peak = max(left_peak, right_peak)
        
        # Normalize if we have signal
        if overall_peak > 0:
            left = left / overall_peak
            right = right / overall_peak
            
        return left, right
        
    def _update_phase_correlation(self, left: np.ndarray, right: np.ndarray) -> None:
        """
        Calculate and display phase correlation coefficient.
        
        The phase correlation coefficient indicates how similar the
        left and right channels are:
        - +1.0: Identical signals (mono)
        - 0.0: Uncorrelated signals (wide stereo)
        - -1.0: Inverted signals (mono incompatible)
        
        Args:
            left: Left channel data
            right: Right channel data
        """
        if len(left) > 1 and len(right) > 1:
            try:
                # Calculate Pearson correlation coefficient
                correlation_matrix = np.corrcoef(left, right)
                correlation = correlation_matrix[0, 1]
                
                if not np.isnan(correlation):
                    # Format correlation value
                    phase_text = f'Phase: {correlation:+.3f}'
                    
                    # Color-code based on correlation value
                    if correlation >= PHASE_THRESHOLDS["good"]:
                        color = COLORS["phase_good"]
                    elif correlation >= PHASE_THRESHOLDS["moderate"]:
                        color = COLORS["phase_moderate"] 
                    else:
                        color = COLORS["phase_poor"]
                    
                    # Update display with colored text
                    self.phase_text.setHtml(
                        f'<div style="color: rgb{color}; font-size: 12pt; '
                        f'font-weight: bold;">{phase_text}</div>'
                    )
                else:
                    self.phase_text.setHtml(
                        '<div style="color: rgb(128,128,128); font-size: 12pt;">Phase: ---</div>'
                    )
                    
            except (ValueError, np.linalg.LinAlgError):
                # Handle edge cases (e.g., constant signals)
                self.phase_text.setHtml(
                    '<div style="color: rgb(128,128,128); font-size: 12pt;">Phase: ERR</div>'
                )
                
    def _update_scatter_plot(self, left: np.ndarray, right: np.ndarray) -> None:
        """
        Update the main scatter plot with current audio samples.
        
        Args:
            left: Left channel data
            right: Right channel data
        """
        if len(left) > 0 and len(right) > 0:
            # Create position array for scatter plot (L=X, R=Y)
            positions = np.column_stack((left, right))
            self.scatter.setData(pos=positions)
        else:
            # Clear if no data
            self.scatter.clear()
            
    def _update_trail_effect(self, left: np.ndarray, right: np.ndarray) -> None:
        """
        Update the visual trail effect showing recent audio history.
        
        The trail effect helps visualize the movement and patterns
        in the stereo field over time, making it easier to spot
        periodic or evolving stereo content.
        
        Args:
            left: Left channel data  
            right: Right channel data
        """
        if len(left) > 0 and len(right) > 0:
            # Store current positions for trail effect
            positions = np.column_stack((left, right))
            self.trail_data.append(positions)
            
            # Limit trail history
            if len(self.trail_data) > self.trail_max_frames:
                self.trail_data.pop(0)
                
            # Draw trail curves (most recent to oldest)
            for i, curve in enumerate(self.trail_curves):
                if i < len(self.trail_data):
                    # Get data from trail history (most recent first)
                    trail_positions = self.trail_data[-(i+1)]
                    
                    if len(trail_positions) > 1:
                        # Draw trail curve
                        curve.setData(trail_positions[:, 0], trail_positions[:, 1])
                    else:
                        curve.clear()
                else:
                    curve.clear()
        else:
            # Clear all trails if no data
            for curve in self.trail_curves:
                curve.clear()
                
    def clear(self) -> None:
        """Clear all visualization elements."""
        super().clear()
        self.scatter.clear()
        for curve in self.trail_curves:
            curve.clear()
        self.trail_data.clear()
        
    def reset(self) -> None:
        """Reset the goniometer to initial state."""
        self.clear()
        self.phase_text.setHtml(
            '<div style="color: rgb(200,200,200); font-size: 12pt;">Phase: ---</div>'
        )