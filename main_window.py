"""
Main application window for the YouTube Goniometer.

This module contains the primary GUI window that orchestrates the audio player,
YouTube downloader, and goniometer visualization components.
"""

import os
from typing import Optional

import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui

from config import (
    APP_INFO, UI_CONFIG, SHORTCUTS, TIMER_CONFIG, 
    get_stylesheet
)
from audio_player import AudioPlayer, AudioPlayerError
from visualizers import GonioViz
from youtube_utils import YouTubeDownloadError


class GoniometerWindow(QtWidgets.QMainWindow):
    """
    Main application window for the YouTube Goniometer.
    
    This window provides the primary interface for loading YouTube videos,
    controlling playback, and displaying the goniometer visualization.
    
    Features:
        - YouTube URL input and audio downloading
        - Play/pause/reset audio controls
        - Real-time goniometer visualization
        - Keyboard shortcuts for all major functions
        - Professional audio analysis interface
    """

    def __init__(self) -> None:
        """Initialize the main application window."""
        super().__init__()
        
        # Window setup
        self._setup_window()
        
        # Initialize audio player
        self.player = AudioPlayer()
        self.player.frame_available.connect(self.on_audio_block)
        self.player.state_changed.connect(self.on_state_changed)
        
        # Initialize play action for later reference
        self.play_action: Optional[QtGui.QAction] = None
        
        # Create UI components
        self._create_ui()
        
        # Setup timers and updates
        self._setup_timers()
        
        # Track last audio data for visualization
        self._last_block: Optional[np.ndarray] = None

    def _setup_window(self) -> None:
        """Configure the main window properties."""
        self.setWindowTitle(f"{APP_INFO['name']} v{APP_INFO['version']}")
        window_size = UI_CONFIG["window_size"]
        minimum_size = UI_CONFIG["minimum_size"]
        self.resize(int(window_size[0]), int(window_size[1]))
        self.setMinimumSize(int(minimum_size[0]), int(minimum_size[1]))
        
        # Apply stylesheet from configuration
        self.setStyleSheet(get_stylesheet())

    def _create_ui(self) -> None:
        """Create and layout all UI components."""
        # Central widget and main layout
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        main_margin = int(UI_CONFIG["margins"]["main_layout"])
        layout.setContentsMargins(main_margin, main_margin, main_margin, main_margin)

        # Title label for showing video/track name
        self.title_label = QtWidgets.QLabel("No YouTube video loaded")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_font_size = str(UI_CONFIG["font_sizes"]["title"])
        border_radius = str(UI_CONFIG["border_radius"])
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-size: {title_font_size};
                font-weight: bold;
                color: white;
                padding: 8px;
                margin: 4px;
                border: 1px solid rgba(80, 85, 100, 100);
                border-radius: {border_radius};
                background: rgba(40, 45, 60, 150);
            }}
        """)
        layout.addWidget(self.title_label)

        # Goniometer visualization (main content area)
        self.gonio = GonioViz(int(self.player.samplerate))
        layout.addWidget(self.gonio, 1)  # Give it all available space

        # Status bar and toolbar
        self.status = self.statusBar()
        self.status.showMessage("Ready - Press 'O' to open YouTube URL")
        self._create_toolbar()

    def _create_toolbar(self) -> None:
        """Create the main toolbar with playback controls."""
        toolbar = QtWidgets.QToolBar("Main Controls")
        self.addToolBar(toolbar)
        
        # Open YouTube URL action
        open_action = QtGui.QAction('🎵 Open YouTube URL (O)', self)
        open_action.setShortcut(QtGui.QKeySequence(SHORTCUTS["open_url"]))
        open_action.setToolTip(f"Open YouTube URL [{SHORTCUTS['open_url']}]")
        open_action.triggered.connect(self.open_youtube_dialog)
        toolbar.addAction(open_action)
        
        # Set fixed width for open button
        open_button = toolbar.widgetForAction(open_action)
        if open_button:
            open_button.setMinimumWidth(180)  # Wider for longer text
            open_button.setMaximumWidth(180)

        toolbar.addSeparator()

        # Play/Pause action
        self.play_action = QtGui.QAction('⏯️ Play/Pause (Space)', self)
        self.play_action.setShortcut(QtGui.QKeySequence(SHORTCUTS["play_pause"]))
        self.play_action.setToolTip(f"Play/Pause [{SHORTCUTS['play_pause']}]")
        self.play_action.triggered.connect(self.toggle_playback)
        toolbar.addAction(self.play_action)
        
        # Set fixed width for play/pause button to prevent shifting
        play_button = toolbar.widgetForAction(self.play_action)
        if play_button:
            play_button.setMinimumWidth(150)  # Wider to accommodate both play/pause states
            play_button.setMaximumWidth(150)

        # Reset action
        reset_action = QtGui.QAction('🔄 Reset (R)', self)
        reset_action.setShortcut(QtGui.QKeySequence(SHORTCUTS["reset"]))
        reset_action.setToolTip(f"Reset to beginning [{SHORTCUTS['reset']}]")
        reset_action.triggered.connect(self.reset_playback)
        toolbar.addAction(reset_action)
        
        # Set fixed width for reset button
        reset_button = toolbar.widgetForAction(reset_action)
        if reset_button:
            reset_button.setMinimumWidth(110)  # Slightly wider
            reset_button.setMaximumWidth(110)

        toolbar.addSeparator()

        # Application info action
        info_action = QtGui.QAction('ℹ️ About', self)
        info_action.setToolTip("About this application")
        info_action.triggered.connect(self.show_about_dialog)
        toolbar.addAction(info_action)

    def _setup_timers(self) -> None:
        """Setup timers for periodic updates."""
        # Visualization update timer
        self.redraw_timer = QtCore.QTimer(self)
        self.redraw_timer.setInterval(TIMER_CONFIG["redraw_interval"])
        self.redraw_timer.timeout.connect(self._update_visualization)
        self.redraw_timer.start()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Handle keyboard shortcuts.
        
        Args:
            event: The key press event
        """
        key = event.key()
        
        if key == QtCore.Qt.Key.Key_Space:
            self.toggle_playback()
        elif key == QtCore.Qt.Key.Key_O:
            self.open_youtube_dialog()
        elif key == QtCore.Qt.Key.Key_R:
            self.reset_playback()
        elif event.matches(QtGui.QKeySequence.StandardKey.Quit):
            self.close()
        else:
            super().keyPressEvent(event)

    def open_youtube_dialog(self) -> None:
        """
        Show dialog to input YouTube URL and load the audio.
        
        This method presents a text input dialog for the user to enter
        a YouTube URL, then attempts to download and load the audio.
        """
        # Create a custom dialog with smaller example text
        dialog = QtWidgets.QInputDialog(self)
        dialog.setWindowTitle('YouTube URL Input')
        dialog.setLabelText('Enter YouTube URL:')
        dialog.setTextValue('')
        
        # Add smaller example text by creating a custom widget
        examples_text = ('Examples: youtube.com/watch?v=..., youtu.be/..., music.youtube.com/...')
        
        # Get the dialog layout and add example text with smaller font
        layout = dialog.layout()
        if layout:
            example_label = QtWidgets.QLabel(examples_text)
            example_label.setStyleSheet("font-size: 9pt; color: gray; margin-top: 5px;")
            example_label.setWordWrap(True)
            layout.addWidget(example_label)
        
        accepted = dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted
        url = dialog.textValue() if accepted else ""
        
        if accepted and url.strip():
            self._load_audio_source(url.strip())

    def _load_audio_source(self, path: str) -> None:
        """
        Load an audio source (YouTube URL or local file).
        
        Args:
            path: YouTube URL or local file path to load
        """
        try:
            # Show loading message
            self.status.showMessage("Loading audio from YouTube...")
            self.title_label.setText("Loading...")
            
            # Allow GUI to update
            QtWidgets.QApplication.processEvents()
            
            # Close any existing audio
            self.player.close()
            
            # Load new audio source
            loaded_path, title = self.player.open(path)
            
            # Update goniometer with new sample rate
            self.gonio.samplerate = int(self.player.samplerate)
            
            # Start playback
            self.player.play()
            
            # Update UI with loaded content
            display_title = title if title else os.path.basename(loaded_path)
            self.title_label.setText(display_title)
            
            # Update status with audio info
            channels_text = "stereo" if self.player.channels == 2 else f"{self.player.channels}ch"
            self.status.showMessage(
                f"Playing: {display_title} — {self.player.samplerate} Hz, {channels_text}"
            )
            
        except YouTubeDownloadError as e:
            self._show_error("YouTube Download Error", str(e))
        except AudioPlayerError as e:
            self._show_error("Audio Error", str(e))
        except Exception as e:
            self._show_error("Unexpected Error", f"An unexpected error occurred: {str(e)}")

    def toggle_playback(self) -> None:
        """
        Toggle between play and pause states.
        
        If audio is currently playing, it will be paused.
        If audio is paused or stopped, it will start playing.
        """
        if not self.player.is_running:
            self.player.play()
        elif self.player.is_paused:
            self.player.play()
        else:
            self.player.pause()

    def reset_playback(self) -> None:
        """
        Reset audio playback to the beginning.
        
        This stops current playback and resets the position to the start
        of the audio file.
        """
        self.player.reset()
        self.status.showMessage("Reset to beginning", TIMER_CONFIG["status_message_timeout"])

    def show_about_dialog(self) -> None:
        """Show information about the application."""
        about_text = f"""
        <h2>{APP_INFO['name']}</h2>
        <p><b>Version:</b> {APP_INFO['version']}</p>
        <p><b>Description:</b> {APP_INFO['description']}</p>
        <br>
        <p>{APP_INFO['copyright']}</p>
        <br>
        <p><b>Features:</b></p>
        <ul>
        <li>Real-time goniometer visualization</li>
        <li>YouTube audio downloading and playback</li>
        <li>Professional stereo field analysis</li>
        <li>Phase correlation monitoring</li>
        </ul>
        <br>
        <p><b>Keyboard Shortcuts:</b></p>
        <ul>
        <li><b>O</b> - Open YouTube URL</li>
        <li><b>Space</b> - Play/Pause</li>
        <li><b>R</b> - Reset to beginning</li>
        </ul>
        """
        
        QtWidgets.QMessageBox.about(self, f"About {APP_INFO['name']}", about_text)

    @QtCore.Slot(np.ndarray)
    def on_audio_block(self, data: np.ndarray) -> None:
        """
        Handle incoming audio data from the player.
        
        Args:
            data: Audio data array from the player
        """
        self._last_block = data
        # Update goniometer immediately for responsiveness
        self.gonio.update_audio(data)

    @QtCore.Slot(bool)
    def on_state_changed(self, playing: bool) -> None:
        """
        Handle playback state changes.
        
        Args:
            playing: True if audio is playing, False if paused/stopped
        """
        state_text = "Playing" if playing else "Paused"
        self.status.showMessage(state_text, TIMER_CONFIG["status_message_timeout"])
        
        # Update play button text/icon based on state
        if self.play_action is not None:
            if playing:
                self.play_action.setText('⏸️ Pause (Space)')
                self.play_action.setToolTip(f"Pause [{SHORTCUTS['play_pause']}]")
            else:
                self.play_action.setText('▶️ Play (Space)')
                self.play_action.setToolTip(f"Play [{SHORTCUTS['play_pause']}]")

    def _update_visualization(self) -> None:
        """
        Periodic update for visualization components.
        
        This method is called by a timer to ensure smooth visualization
        updates even when no new audio data is available.
        """
        if self._last_block is not None:
            self.gonio.update_audio(self._last_block)

    def _show_error(self, title: str, message: str) -> None:
        """
        Display an error message to the user.
        
        Args:
            title: Error dialog title
            message: Error message text
        """
        self.status.showMessage("Error occurred", TIMER_CONFIG["status_message_timeout"])
        self.title_label.setText("Error loading audio")
        
        QtWidgets.QMessageBox.critical(self, title, message)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Handle application close event.
        
        Args:
            event: The close event
        """
        # Clean up audio resources
        self.player.close()
        
        # Stop timers
        self.redraw_timer.stop()
        
        # Accept the close event
        event.accept()