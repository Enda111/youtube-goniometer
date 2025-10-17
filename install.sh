#!/bin/bash
# Installation script for YouTube Goniometer on Linux/macOS

echo "Installing YouTube Goniometer..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"
if [ $? -ne 0 ]; then
    echo "ERROR: Python 3.8 or higher is required"
    python3 --version
    exit 1
fi

echo "Python version check passed"
echo

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo
echo "Installation complete!"
echo
echo "To run YouTube Goniometer:"
echo "  python3 app.py"
echo
echo "Or run: ./run.sh"
echo