"""
Main calculator window with display, buttons, and mode selector.
"""

import customtkinter as ctk
from src.calculator.ui.display import DisplayPanel
from src.calculator.ui.button_panel import ButtonPanel
from src.calculator.config.locale import WINDOW_TITLE, BTN_MODE_BASIC, BTN_MODE_SCIENTIFIC
from src.calculator.config.constants import (
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    WINDOW_DEFAULT_GEOMETRY
)


class CalculatorWindow(ctk.CTk):
    """
    Main calculator window with dark theme and responsive grid layout.
    """

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_DEFAULT_GEOMETRY)
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Mode selector (segmented button)
        self.mode_selector = ctk.CTkSegmentedButton(
            self,
            values=[BTN_MODE_BASIC, BTN_MODE_SCIENTIFIC],
            command=self._on_mode_change
        )
        self.mode_selector.set(BTN_MODE_BASIC)
        self.mode_selector.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Display panel
        self.display = DisplayPanel(self)
        self.display.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Button panel
        self.button_panel = ButtonPanel(self)
        self.button_panel.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Configure grid weights for responsive resizing
        self.grid_rowconfigure(0, weight=0)  # Mode selector fixed height
        self.grid_rowconfigure(1, weight=0)  # Display fixed height
        self.grid_rowconfigure(2, weight=1)  # Buttons expand
        self.grid_columnconfigure(0, weight=1)

        # Callbacks (set by controller)
        self.button_callback = None
        self.mode_callback = None
        self.angle_mode_callback = None

    def _on_mode_change(self, value):
        """Handle mode selector change."""
        mode = "scientific" if value == BTN_MODE_SCIENTIFIC else "basic"
        self.button_panel.set_mode(mode)
        if self.mode_callback:
            self.mode_callback(mode)

    def set_button_callback(self, callback):
        """Set callback for button clicks."""
        self.button_callback = callback
        self.button_panel.set_callback(callback)

    def set_mode_callback(self, callback):
        """Set callback for mode changes."""
        self.mode_callback = callback

    def set_angle_mode_callback(self, callback):
        """Set callback for angle mode changes."""
        self.angle_mode_callback = callback
        self.display.set_angle_mode_callback(callback)

    def get_result(self):
        """Get current result text (for clipboard operations)."""
        return self.display.get_result()

    def update_expression(self, text):
        """Update expression display."""
        self.display.update_expression(text)

    def update_result(self, text):
        """Update result display."""
        self.display.update_result(text)
