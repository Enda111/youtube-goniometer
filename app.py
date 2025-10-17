#!/usr/bin/env python3
"""
Entry point for the YouTube Goniometer application.

This script initializes the Qt application and launches the main window.
Run this file to start the goniometer application.
"""

import sys
from PySide6 import QtWidgets
import pyqtgraph as pg  # type: ignore

from main_window import GoniometerWindow
from config import APP_INFO


def main() -> None:
    """
    Main entry point for the YouTube Goniometer application.
    
    This function:
    1. Creates the Qt application instance
    2. Configures pyqtgraph for optimal rendering
    3. Creates and shows the main window
    4. Starts the Qt event loop
    
    Returns:
        None
        
    Exit Codes:
        0: Normal exit
        1: Application error or exception
    """
    try:
        # Create Qt application instance
        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationName(APP_INFO["name"])
        app.setApplicationVersion(APP_INFO["version"])
        app.setOrganizationName(APP_INFO["author"])
        
        # Configure pyqtgraph for better rendering
        pg.setConfigOptions(
            antialias=True,          # Enable antialiasing for smoother plots
            useOpenGL=False,         # Disable OpenGL for compatibility
            background='k',          # Default background color
            foreground='w'           # Default foreground color
        )
        
        # Create and show main window
        window = GoniometerWindow()
        window.show()
        
        # Start Qt event loop
        sys.exit(app.exec())
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()