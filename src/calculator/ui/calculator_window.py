"""
Main calculator window with display, buttons, and mode selector.
"""

import customtkinter as ctk
from src.calculator.ui.display import DisplayPanel
from src.calculator.ui.button_panel import ButtonPanel
from src.calculator.ui.history_panel import HistoryPanel
from src.calculator.config.locale import WINDOW_TITLE, BTN_MODE_BASIC, BTN_MODE_SCIENTIFIC
from src.calculator.config.constants import (
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    KEYBOARD_CHARS,
    WINDOW_WITH_HISTORY_WIDTH,
    WINDOW_WITH_HISTORY_MIN_WIDTH,
    HISTORY_PANEL_WIDTH
)


class CalculatorWindow(ctk.CTk):
    """
    Main calculator window with dark theme and responsive grid layout.
    """

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WITH_HISTORY_WIDTH}x600")
        self.minsize(WINDOW_WITH_HISTORY_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Create left column frame for calculator
        self.calc_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.calc_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Mode selector (segmented button)
        self.mode_selector = ctk.CTkSegmentedButton(
            self.calc_frame,
            values=[BTN_MODE_BASIC, BTN_MODE_SCIENTIFIC],
            command=self._on_mode_change
        )
        self.mode_selector.set(BTN_MODE_BASIC)
        self.mode_selector.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="ew")

        # Display panel
        self.display = DisplayPanel(self.calc_frame)
        self.display.grid(row=1, column=0, padx=0, pady=(0, 10), sticky="ew")

        # Button panel
        self.button_panel = ButtonPanel(self.calc_frame)
        self.button_panel.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")

        # Configure calc_frame grid weights
        self.calc_frame.grid_rowconfigure(0, weight=0)  # Mode selector fixed height
        self.calc_frame.grid_rowconfigure(1, weight=0)  # Display fixed height
        self.calc_frame.grid_rowconfigure(2, weight=1)  # Buttons expand
        self.calc_frame.grid_columnconfigure(0, weight=1)

        # History panel (right column)
        self.history_panel = HistoryPanel(self)
        self.history_panel.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")

        # Configure main window grid weights (2-column layout)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Calculator column expands
        self.grid_columnconfigure(1, weight=0)  # History column fixed width

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

    # History panel convenience methods

    def add_history_entry(self, expression, result):
        """Add entry to history panel."""
        self.history_panel.add_entry(expression, result)

    def set_history_recall_callback(self, callback):
        """Set callback for history entry clicks."""
        self.history_panel.set_recall_callback(callback)

    def set_history_clear_callback(self, callback):
        """Set callback for history clear button."""
        self.history_panel.set_clear_callback(callback)

    def clear_history(self):
        """Clear all history entries."""
        self.history_panel.clear_history()
