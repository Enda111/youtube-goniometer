#!/bin/bash
# Run script for YouTube Goniometer on Linux/macOS

echo "Starting YouTube Goniometer..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please run ./install.sh first"
    exit 1
fi

# Run the application
python3 app.py