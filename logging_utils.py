"""
Logging and Error Handling Utilities for YouTube Goniometer.

This module provides centralized logging configuration and error handling
utilities for the entire application. It sets up structured logging with
appropriate levels and formatters for development and production use.
"""

import logging
import sys
import traceback
from pathlib import Path
from typing import Optional, Any

from config import APP_INFO


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Configure application-wide logging.
    
    Args:
        level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        log_file: Optional path to log file. If None, no file logging.
        console_output: Whether to output logs to console
        
    Returns:
        Configured logger instance
        
    Example:
        >>> logger = setup_logging(level="DEBUG", log_file="goniometer.log")
        >>> logger.info("Application started")
    """
    # Create main logger
    logger = logging.getLogger(APP_INFO["name"])
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)  # Always debug level for file
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.debug("Debug message")
    """
    if name is None:
        name = APP_INFO["name"]
    return logging.getLogger(name)


class ErrorHandler:
    """
    Centralized error handling and reporting.
    
    This class provides methods for handling different types of errors
    with appropriate logging and user notification strategies.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize error handler.
        
        Args:
            logger: Optional logger instance. If None, creates default logger.
        """
        self.logger = logger or get_logger("ErrorHandler")
    
    def handle_audio_error(self, error: Exception, context: str = "") -> str:
        """
        Handle audio-related errors.
        
        Args:
            error: The exception that occurred
            context: Additional context about when/where the error occurred
            
        Returns:
            User-friendly error message
        """
        error_msg = f"Audio Error: {str(error)}"
        if context:
            error_msg = f"{context}: {error_msg}"
            
        self.logger.error(error_msg, exc_info=True)
        
        # Return user-friendly message
        if "sounddevice" in str(error).lower():
            return ("Audio device error. Please check that your audio device "
                   "is connected and not being used by another application.")
        elif "soundfile" in str(error).lower():
            return ("Audio file error. The file may be corrupted or in an "
                   "unsupported format.")
        else:
            return f"An audio error occurred: {str(error)}"
    
    def handle_youtube_error(self, error: Exception, url: str = "") -> str:
        """
        Handle YouTube download errors.
        
        Args:
            error: The exception that occurred
            url: The YouTube URL that failed (for logging)
            
        Returns:
            User-friendly error message
        """
        context = f"YouTube download failed for URL: {url}" if url else "YouTube download failed"
        self.logger.error(f"{context}: {str(error)}", exc_info=True)
        
        error_str = str(error).lower()
        
        if "network" in error_str or "connection" in error_str:
            return ("Network error. Please check your internet connection "
                   "and try again.")
        elif "video unavailable" in error_str or "private" in error_str:
            return ("This video is not available. It may be private, "
                   "restricted, or deleted.")
        elif "ffmpeg" in error_str:
            return ("FFmpeg not found. Please install FFmpeg and ensure "
                   "it's accessible from your PATH.")
        elif "format" in error_str:
            return ("No suitable audio format found for this video. "
                   "Try a different video.")
        else:
            return f"YouTube download failed: {str(error)}"
    
    def handle_gui_error(self, error: Exception, widget: str = "") -> str:
        """
        Handle GUI-related errors.
        
        Args:
            error: The exception that occurred
            widget: Name of the widget/component that failed
            
        Returns:
            User-friendly error message
        """
        context = f"GUI error in {widget}" if widget else "GUI error"
        self.logger.error(f"{context}: {str(error)}", exc_info=True)
        
        if "qt" in str(error).lower() or "pyside" in str(error).lower():
            return ("A GUI error occurred. Please restart the application.")
        else:
            return f"Interface error: {str(error)}"
    
    def handle_unexpected_error(self, error: Exception, context: str = "") -> str:
        """
        Handle unexpected/uncategorized errors.
        
        Args:
            error: The exception that occurred
            context: Additional context about the operation
            
        Returns:
            User-friendly error message
        """
        full_context = f"Unexpected error in {context}" if context else "Unexpected error"
        self.logger.critical(f"{full_context}: {str(error)}", exc_info=True)
        
        # Log full traceback for debugging
        self.logger.debug("Full traceback:", exc_info=True)
        
        return (f"An unexpected error occurred: {str(error)}\n\n"
               f"Please check the log file for details.")
    
    def log_system_info(self) -> None:
        """Log system information for debugging purposes."""
        import platform
        try:
            import sounddevice as sd  # type: ignore
            import soundfile as sf  # type: ignore
            import pyqtgraph as pg  # type: ignore
            from PySide6 import QtCore
            
            self.logger.info("=== System Information ===")
            self.logger.info(f"Platform: {platform.platform()}")
            self.logger.info(f"Python: {platform.python_version()}")
            self.logger.info(f"Architecture: {platform.architecture()}")
            
            self.logger.info("=== Audio System ===")
            try:
                devices = sd.query_devices()
                default_device = sd.default.device
                self.logger.info(f"Default audio device: {default_device}")
                self.logger.info(f"Available devices: {len(devices)}")
            except Exception as e:
                self.logger.warning(f"Could not query audio devices: {e}")
            
            self.logger.info("=== Library Versions ===")
            self.logger.info(f"SoundDevice: {getattr(sd, '__version__', 'unknown')}")
            self.logger.info(f"SoundFile: {getattr(sf, '__version__', 'unknown')}")
            self.logger.info(f"PyQtGraph: {getattr(pg, '__version__', 'unknown')}")
            self.logger.info(f"PySide6: {getattr(QtCore, '__version__', 'unknown')}")
            
        except Exception as e:
            self.logger.warning(f"Could not log complete system info: {e}")


def log_exception(logger: logging.Logger, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
    """
    Custom exception handler that logs unhandled exceptions.
    
    This function can be set as sys.excepthook to catch and log
    all unhandled exceptions in the application.
    
    Args:
        logger: Logger instance to use
        exc_type: Exception type
        exc_value: Exception value
        exc_traceback: Exception traceback
    """
    if issubclass(exc_type, KeyboardInterrupt):
        # Don't log keyboard interrupts
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger.critical(
        "Unhandled exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )


def setup_exception_logging(logger: logging.Logger) -> None:
    """
    Set up global exception logging.
    
    Args:
        logger: Logger instance to use for exception logging
    """
    def exception_handler(exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        log_exception(logger, exc_type, exc_value, exc_traceback)
    
    sys.excepthook = exception_handler


class LoggingContext:
    """
    Context manager for logging operations with timing.
    
    Example:
        >>> with LoggingContext(logger, "Loading audio"):
        ...     load_audio_file(path)
    """
    
    def __init__(self, logger: logging.Logger, operation: str, level: int = logging.INFO):
        """
        Initialize logging context.
        
        Args:
            logger: Logger instance
            operation: Description of the operation being logged
            level: Logging level for the messages
        """
        self.logger = logger
        self.operation = operation
        self.level = level
        self.start_time: Optional[float] = None
    
    def __enter__(self) -> 'LoggingContext':
        """Enter the context and log start message."""
        import time
        self.start_time = time.time()
        self.logger.log(self.level, f"Starting: {self.operation}")
        return self
    
    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        """Exit the context and log completion/error message."""
        import time
        duration = time.time() - self.start_time if self.start_time else 0
        
        if exc_type is None:
            self.logger.log(self.level, f"Completed: {self.operation} ({duration:.2f}s)")
        else:
            self.logger.error(
                f"Failed: {self.operation} after {duration:.2f}s - {exc_value}",
                exc_info=True
            )
        
        # Don't suppress exceptions
        pass