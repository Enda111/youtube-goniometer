"""
Configuration settings for the YouTube Goniometer application.

This module contains all configurable constants, colors, and settings
used throughout the application for easy customization and maintenance.
"""

import os
from typing import Dict, Any, Tuple

# Audio Configuration
AUDIO_CONFIG: Dict[str, Any] = {
    "default_samplerate": 44100,
    "default_channels": 2,
    "blocksize": 1024,
    "max_gonio_points": 800,
    "audio_smoothing_alpha": 0.8,
}

# YouTube Download Configuration
YOUTUBE_CONFIG: Dict[str, str] = {
    "temp_prefix": "audviz_",
    "audio_format": "bestaudio/best",
    "output_format": "wav",
    "audio_quality": "0",  # Best quality
    "resample_rate": "44100",
    "channels": "2",  # Stereo
}

# FFmpeg Configuration
def get_ffmpeg_path() -> str:
    """Get the default FFmpeg installation path for the current platform."""
    import platform
    import shutil
    
    # First try to find ffmpeg in PATH
    ffmpeg_exe = shutil.which('ffmpeg')
    if ffmpeg_exe:
        return os.path.dirname(ffmpeg_exe)
    
    # Platform-specific fallback paths
    system = platform.system()
    if system == "Windows":
        username = os.environ.get('USERNAME', 'default')
        return (f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\WinGet\\Packages\\"
                f"Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-8.0-full_build\\bin")
    elif system == "Darwin":  # macOS
        return "/opt/homebrew/bin"  # Homebrew default
    else:  # Linux and others
        return "/usr/bin"

FFMPEG_CONFIG: Dict[str, Any] = {
    "default_path": get_ffmpeg_path(),
    "timeout": 30.0,  # Download timeout in seconds
}

# UI Colors and Styling
COLORS: Dict[str, Any] = {
    # Main window background gradient
    "bg_gradient_start": (25, 30, 45),
    "bg_gradient_end": (45, 50, 65),
    
    # Toolbar and UI elements
    "toolbar_bg": (60, 65, 80, 200),
    "button_bg": (80, 85, 100, 180),
    "button_hover": (100, 105, 120, 220),
    "button_border": (120, 125, 140, 100),
    "status_bg": (40, 45, 60, 200),
    
    # Visualizer colors
    "plot_bg": (20, 20, 30),
    "grid_color": (80, 80, 100),
    "center_lines": (80, 80, 100),
    "diagonal_lines": (60, 60, 80),
    
    # Goniometer specific colors
    "scatter_main": (0, 255, 0, 150),
    "trail_colors": [
        (0, 255, 0, 100),   # Most recent
        (0, 200, 50, 70),
        (0, 150, 100, 50),
        (0, 100, 150, 30),
        (0, 50, 200, 15),   # Oldest
    ],
    
    # Phase correlation colors
    "phase_good": (0, 255, 0),      # >0.8 correlation
    "phase_moderate": (255, 255, 0), # 0.3-0.8 correlation  
    "phase_poor": (255, 0, 0),      # <0.3 correlation
    
    # Text colors
    "text_primary": (255, 255, 255),
    "text_secondary": (200, 200, 200),
}

# UI Layout Configuration
UI_CONFIG: Dict[str, Any] = {
    "window_size": (800, 800),  # Square window for equal L&R channel display
    "minimum_size": (800, 500),
    "font_sizes": {
        "title": "14pt",
        "button": "10pt",
        "status": "9pt",
        "phase_indicator": "12pt",
    },
    "margins": {
        "main_layout": 8,
        "toolbar_spacing": 8,
        "plot_margins": (10, 10, 10, 10),
    },
    "button_padding": "6px 12px",
    "border_radius": "4px",
}

# Goniometer Display Configuration
GONIOMETER_CONFIG: Dict[str, Any] = {
    "plot_range": (-1.0, 1.0),  # Eliminate dead space, use full normalized audio range
    "aspect_locked": True,
    "show_grid": True,
    "grid_alpha": 0.3,
    "scatter_size": 3,
    "max_points": 800,
    "trail_max_frames": 5,
    "center_line_style": "dash",
    "diagonal_line_style": "dot",
    "line_widths": {
        "center": 1,
        "diagonal": 1,
        "trail": 1,
    },
}

# Phase Correlation Thresholds
PHASE_THRESHOLDS: Dict[str, float] = {
    "good": 0.8,      # Green - excellent stereo correlation
    "moderate": 0.3,  # Yellow - acceptable correlation
    # Below moderate is poor (red)
}

# Keyboard Shortcuts
SHORTCUTS: Dict[str, str] = {
    "open_url": "O",
    "play_pause": "Space", 
    "reset": "R",
    "quit": "Ctrl+Q",
}

# Timer Configuration
TIMER_CONFIG: Dict[str, int] = {
    "redraw_interval": 30,  # milliseconds
    "status_message_timeout": 1500,  # milliseconds
    "restart_delay": 50,  # milliseconds
}

# Error Messages
ERROR_MESSAGES: Dict[str, str] = {
    "no_ffmpeg": "FFmpeg not found. Please install FFmpeg and ensure it's in your PATH.",
    "youtube_download_failed": "Failed to download audio from YouTube URL.",
    "audio_file_error": "Could not open audio file.",
    "playback_error": "Audio playback error occurred.",
    "invalid_url": "Please enter a valid YouTube URL.",
    "network_error": "Network error. Please check your internet connection.",
}

# Application Metadata
APP_INFO: Dict[str, str] = {
    "name": "YouTube Goniometer",
    "version": "1.0.0",
    "description": "Professional goniometer for YouTube audio analysis",
    "author": "Enda111",
    "copyright": "© 2024 Enda111",
}

def get_stylesheet() -> str:
    """Generate the main application stylesheet from configuration."""
    bg_start = COLORS["bg_gradient_start"]
    bg_end = COLORS["bg_gradient_end"]
    toolbar_bg = COLORS["toolbar_bg"]
    button_bg = COLORS["button_bg"]
    button_hover = COLORS["button_hover"]
    button_border = COLORS["button_border"]
    status_bg = COLORS["status_bg"]
    
    # Ensure color tuples are properly formatted for CSS
    bg_start_rgba = f"rgba({bg_start[0]}, {bg_start[1]}, {bg_start[2]}, 255)"
    bg_end_rgba = f"rgba({bg_end[0]}, {bg_end[1]}, {bg_end[2]}, 255)"
    toolbar_rgba = f"rgba({toolbar_bg[0]}, {toolbar_bg[1]}, {toolbar_bg[2]}, {toolbar_bg[3]})"
    button_rgba = f"rgba({button_bg[0]}, {button_bg[1]}, {button_bg[2]}, {button_bg[3]})"
    button_hover_rgba = f"rgba({button_hover[0]}, {button_hover[1]}, {button_hover[2]}, {button_hover[3]})"
    button_border_rgba = f"rgba({button_border[0]}, {button_border[1]}, {button_border[2]}, {button_border[3]})"
    status_rgba = f"rgba({status_bg[0]}, {status_bg[1]}, {status_bg[2]}, {status_bg[3]})"
    
    # Get UI configuration values
    title_font_size = str(UI_CONFIG["font_sizes"]["title"])
    toolbar_spacing = str(UI_CONFIG["margins"]["toolbar_spacing"])
    border_radius = str(UI_CONFIG["border_radius"])
    button_padding = str(UI_CONFIG["button_padding"])
    button_font_size = str(UI_CONFIG["font_sizes"]["button"])
    status_font_size = str(UI_CONFIG["font_sizes"]["status"])
    
    return f"""
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {bg_start_rgba},
                stop:1 {bg_end_rgba});
        }}
        QLabel {{
            color: white;
            font-size: {title_font_size}px;
            font-weight: bold;
            padding: 8px;
        }}
        QToolBar {{
            background: {toolbar_rgba};
            border: none;
            spacing: {toolbar_spacing}px;
            padding: 4px;
        }}
        QToolBar QToolButton {{
            background: {button_rgba};
            color: white;
            border: 1px solid {button_border_rgba};
            border-radius: {border_radius}px;
            padding: {button_padding}px;
            font-weight: bold;
            font-size: {button_font_size}px;
            text-align: center;
            min-width: 100px;
        }}
        QToolBar QToolButton:hover {{
            background: {button_hover_rgba};
        }}
        QStatusBar {{
            background: {status_rgba};
            color: white;
            border-top: 1px solid rgba(80, 85, 100, 100);
            font-size: {status_font_size}px;
        }}
    """