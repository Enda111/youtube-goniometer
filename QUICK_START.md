# Quick Start Distribution Guide

## For End Users (Non-Programmers)

### Windows Users
1. **Download and run** `install.bat`
2. **Double-click** `run.bat` to start the application

### Mac/Linux Users
1. **Run** `chmod +x install.sh && ./install.sh`
2. **Run** `./run.sh` to start the application

## For Developers

### Install as Python Package
```bash
pip install -e .
```

### Run Development Version
```bash
python app.py
```

### Build Distribution
```bash
python -m build
```

## What You Need to Distribute

### Essential Files
- All `.py` files (app.py, config.py, etc.)
- `visualizers/` folder
- `requirements.txt`
- `pyproject.toml`
- `README.md`
- `LICENSE`

### Easy Installation Scripts
- `install.bat` (Windows)
- `install.sh` (Mac/Linux)
- `run.bat` (Windows)
- `run.sh` (Mac/Linux)

### Distribution Packages
- `dist/youtube_goniometer-1.0.0.tar.gz` (source)
- `dist/youtube_goniometer-1.0.0-py3-none-any.whl` (wheel)

## Distribution Methods

1. **GitHub Release** - Upload all files as a release
2. **PyPI** - `pip install twine && twine upload dist/*`
3. **Direct Download** - Zip folder and share
4. **Executable** - Use PyInstaller for standalone apps

## User Instructions to Include

### Requirements
- Python 3.8 or higher
- FFmpeg (for YouTube audio)

### Installation
```bash
# Easy way
pip install youtube-goniometer

# From source
git clone https://github.com/yourusername/youtube-goniometer.git
cd youtube-goniometer
pip install -e .
```

### Usage
```bash
# Run the app
youtube-goniometer

# Or directly
python app.py
```