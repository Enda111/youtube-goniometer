"""
YouTube Goniometer - Backward Compatibility Entry Point

This is a backward compatibility entry point that launches the refactored
application. The main application code has been reorganized into separate
modules for better maintainability.

For the new entry point, use: python app.py
"""

# Import and run the main application
from app import main

if __name__ == '__main__':
    main()