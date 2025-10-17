# YouTube Goniometer

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A professional-grade goniometer for real-time stereo field analysis of YouTube audio content. This application provides broadcast-quality visualization tools used in professional audio production, mastering, and broadcast environments.

## Overview

The YouTube Goniometer is a specialized audio analysis tool that visualizes the relationship between left and right channels in stereo audio. It plots left channel amplitude on the X-axis and right channel amplitude on the Y-axis, creating patterns that reveal stereo imaging, phase relationships, and mono compatibility characteristics.

## Features

### Core Functionality
- **YouTube Audio Analysis** - Direct audio streaming from YouTube URLs
- **Professional Goniometer Display** - Broadcast-standard L/R correlation visualization
- **Real-Time Phase Correlation** - Continuous monitoring with color-coded indicators
- **Visual Trail Effects** - Shows recent audio history for pattern recognition
- **Professional Reference Lines** - Industry-standard mono and phase detection guides

### User Interface
- **Clean, Professional Design** - Inspired by broadcast audio equipment
- **Keyboard Shortcuts** - Efficient operation for audio professionals
- **Real-Time Updates** - 30fps visualization for smooth analysis
- **Video Title Display** - Shows actual YouTube video information
- **Status Monitoring** - Real-time playback and analysis information

### Technical Features  
- **High-Performance Rendering** - Optimized for real-time audio analysis
- **Professional Color Coding** - Industry-standard phase correlation indicators
- **Configurable Parameters** - Customizable display and analysis settings
- **Error Handling** - Robust error reporting and recovery
- **Modular Architecture** - Well-organized, maintainable codebase

## Installation

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version  # Should show 3.8+
   ```

2. **FFmpeg** (Required for YouTube audio extraction)
   
   **Windows (recommended):**
   ```bash
   # Using winget (Windows 10/11)
   winget install Gyan.FFmpeg
   
   # Or download from https://ffmpeg.org/download.html
   # Add ffmpeg/bin to your PATH environment variable
   ```
   
   **macOS:**
   ```bash
   # Using Homebrew
   brew install ffmpeg
   ```
   
   **Linux:**
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   
   # Fedora
   sudo dnf install ffmpeg
   
   # Arch Linux
   sudo pacman -S ffmpeg
   ```

### Install YouTube Goniometer

#### Option 1: Clone and Install (Recommended for Development)
```bash
git clone https://github.com/yourusername/youtube-goniometer.git
cd youtube-goniometer
pip install -e .
```

#### Option 2: Direct Installation
```bash
pip install numpy sounddevice soundfile pyqtgraph PySide6 yt-dlp
```

#### Option 3: Development Installation
```bash
git clone https://github.com/yourusername/youtube-goniometer.git
cd youtube-goniometer
pip install -e ".[dev]"  # Includes development tools
```

## Usage

### Basic Usage
```bash
# Run the application
python app.py

# Or if installed as package
youtube-goniometer
```

### Controls

| Key | Action | Description |
|-----|--------|-------------|
| **O** | Open URL | Opens YouTube URL input dialog |
| **Space** | Play/Pause | Toggles audio playback |
| **R** | Reset | Resets playback to beginning |
| **Ctrl+Q** | Quit | Exits the application |

### How to Use

1. **Launch Application**
   ```bash
   python app.py
   ```

2. **Load YouTube Content**
   - Press **O** or click "Open YouTube URL" 
   - Paste any YouTube URL (music, videos, live streams)
   - Wait for audio download and processing

3. **Analyze Audio**
   - Watch the goniometer display for stereo patterns
   - Monitor phase correlation values
   - Use controls to navigate the audio

### Understanding the Goniometer Display

#### Visual Patterns
- **Center Point (0,0)** - Perfect mono signal
- **Horizontal Line** - Only left channel active
- **Vertical Line** - Only right channel active  
- **45° Diagonal (L=R)** - Mono content in both channels
- **-45° Diagonal (L=-R)** - Anti-phase stereo (mono incompatible)
- **Circular Patterns** - Uncorrelated stereo content (wide image)
- **Elliptical Patterns** - Correlated stereo with controlled width

#### Phase Correlation Indicator
The phase correlation coefficient is displayed in the top-left corner:

| Value | Color | Meaning |
|-------|-------|---------|
| **+0.8 to +1.0** | 🟢 Green | Excellent correlation (mono-compatible) |
| **+0.3 to +0.8** | 🟡 Yellow | Good correlation (normal stereo) |
| **0.0 to +0.3** | 🟠 Orange | Moderate correlation (wide stereo) |
| **-0.3 to 0.0** | 🔴 Red | Poor correlation (phase issues) |
| **-1.0 to -0.3** | 🔴 Red | Anti-correlation (mono incompatible) |

#### Reference Lines
- **Dashed Cross** - Center reference (L=0, R=0)
- **Dotted Diagonals** - Mono detection lines

## Professional Applications

This goniometer provides analysis capabilities used in:

### Audio Production
- **Mixing** - Monitor stereo width and imaging during mix sessions
- **Mastering** - Ensure proper stereo correlation for various playback systems
- **Sound Design** - Analyze spatial characteristics of audio elements

### Broadcast & Streaming
- **Broadcast Compliance** - Ensure mono compatibility for AM/FM transmission
- **Streaming Optimization** - Verify audio translates well across platforms
- **Live Sound** - Monitor stereo feeds and detect phase issues

### Quality Control
- **Phase Issue Detection** - Identify anti-correlation problems
- **Mono Compatibility** - Test how stereo content sounds in mono
- **Stereo Width Analysis** - Measure and optimize stereo image

## Configuration

### Audio Settings
Edit `config.py` to customize:
- Sample rates and buffer sizes
- Audio processing parameters  
- Performance optimization settings

### Visual Appearance
Customize colors, sizes, and display options:
- Goniometer colors and trail effects
- UI themes and styling
- Plot ranges and grid settings

### Advanced Configuration
```python
# Example config.py modifications
AUDIO_CONFIG = {
    "default_samplerate": 48000,  # Higher quality
    "blocksize": 512,             # Lower latency  
}

GONIOMETER_CONFIG = {
    "max_points": 1200,           # More detail
    "trail_max_frames": 8,        # Longer trails
}
```

## Development

### Project Structure
```
youtube-goniometer/
├── app.py                 # Main entry point
├── config.py             # Configuration settings
├── audio_player.py       # Audio playback engine
├── youtube_utils.py      # YouTube download utilities
├── main_window.py        # GUI main window
├── logging_utils.py      # Error handling and logging
├── visualizers/          # Visualization components
│   ├── __init__.py
│   ├── base.py          # Base visualizer class
│   └── gonio.py         # Goniometer implementation
├── README.md
├── pyproject.toml       # Project configuration
└── goniometer.py        # Legacy entry point (compatibility)
```

### Running Tests
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

### Code Quality
```bash
# Format code
black .

# Lint code
pylint *.py visualizers/

# Type checking
mypy *.py
```

## Troubleshooting

### Common Issues

**"FFmpeg not found"**
- Ensure FFmpeg is installed and in your PATH
- On Windows, restart your terminal after installing FFmpeg
- Try specifying FFmpeg path in `config.py`

**"Audio device error"**
- Check that your audio device is connected
- Close other applications using audio
- Try different audio device in system settings

**"YouTube download failed"**
- Check internet connection
- Try a different YouTube URL
- Some videos may be region-restricted or private

**"GUI not appearing"**
- Ensure you have a display/desktop environment
- Check Python GUI backend installation
- Try running with different Qt backend

### Debug Mode
```bash
# Run with debug logging
python app.py --log-level DEBUG

# Enable verbose output
python app.py --verbose
```

### Performance Issues
- Reduce `max_points` in `GONIOMETER_CONFIG`
- Increase `blocksize` in `AUDIO_CONFIG`
- Close other applications using audio/video

## Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Format code (`black .`)
7. Submit a pull request

### Development Setup
```bash
git clone https://github.com/yourusername/youtube-goniometer.git
cd youtube-goniometer
pip install -e ".[dev]"
pre-commit install  # If using pre-commit hooks
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **pyqtgraph** - High-performance plotting library
- **yt-dlp** - YouTube download functionality  
- **SoundDevice** - Real-time audio I/O
- **PySide6** - Professional GUI framework
- **Audio engineering community** - For goniometer design principles

## Support

- 📧 **Email**: contact@example.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/youtube-goniometer/issues)
- 📖 **Documentation**: [Project Wiki](https://github.com/yourusername/youtube-goniometer/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/youtube-goniometer/discussions)

---

**Professional Audio Analysis Made Simple** 🎵📊