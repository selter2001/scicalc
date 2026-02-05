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
    WINDOW_DEFAULT_GEOMETRY,
    KEYBOARD_CHARS
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
        self.keyboard_callback = None

        # Bind keyboard shortcuts at window level
        self._bind_keyboard_shortcuts()

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

    def set_keyboard_callback(self, callback):
        """Set callback for keyboard events."""
        self.keyboard_callback = callback

    def _bind_keyboard_shortcuts(self):
        """Bind all keyboard shortcuts at window level."""
        # Enter = calculate (same as =)
        self.bind("<Return>", lambda e: self._on_key("="))

        # Escape = clear (same as C)
        self.bind("<Escape>", lambda e: self._on_key("C"))

        # Backspace = delete last char
        self.bind("<BackSpace>", lambda e: self._on_key("\u232b"))

        # Ctrl+C = copy result to clipboard
        self.bind("<Control-c>", lambda e: self._handle_copy())

        # Ctrl+V = paste from clipboard
        self.bind("<Control-v>", lambda e: self._handle_paste())

        # Number and operator keys -- use lambda default param to avoid closure bug
        for char in KEYBOARD_CHARS:
            self.bind(char, lambda e, c=char: self._on_key(c))

    def _on_key(self, label):
        """Route keyboard input through button callback."""
        if self.button_callback:
            self.button_callback(label)

    def _handle_copy(self):
        """Copy current result to system clipboard."""
        result_text = self.display.get_result()
        if result_text:
            self.clipboard_clear()
            self.clipboard_append(result_text)
        return "break"  # Prevent default Ctrl+C behavior

    def _handle_paste(self):
        """Paste clipboard content into expression."""
        try:
            clipboard_text = self.clipboard_get()
            if clipboard_text and self.button_callback:
                # Strip whitespace before validation (trailing spaces from copy)
                clipboard_text = clipboard_text.strip()
                # Validate: only paste numeric/operator content
                valid_chars = set("0123456789+-*/().eE")
                if clipboard_text and all(c in valid_chars for c in clipboard_text):
                    self.button_callback(clipboard_text)
        except Exception:
            # Clipboard empty or contains non-text data -- ignore silently
            pass
        return "break"  # Prevent default Ctrl+V behavior
