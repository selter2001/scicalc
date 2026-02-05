"""
History panel component for displaying calculation history.
"""

import customtkinter as ctk
from typing import Callable, Optional
from ..config.locale import HIST_TITLE, HIST_CLEAR, HIST_EMPTY
from ..config.constants import HISTORY_PANEL_WIDTH, FONT_HISTORY_TITLE, FONT_HISTORY_ENTRY


class HistoryPanel(ctk.CTkFrame):
    """Scrollable history panel showing previous calculations."""

    def __init__(self, parent):
        super().__init__(parent, width=HISTORY_PANEL_WIDTH, fg_color="transparent")

        self._recall_callback: Optional[Callable[[str], None]] = None
        self._clear_callback: Optional[Callable[[], None]] = None
        self._entry_widgets = []  # Track entry widgets for clearing

        # Header
        title = ctk.CTkLabel(
            self,
            text=HIST_TITLE,
            font=("Arial", FONT_HISTORY_TITLE, "bold")
        )
        title.pack(pady=(5, 10), padx=10, anchor="w")

        # Scrollable frame for entries
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            width=HISTORY_PANEL_WIDTH - 20,
            fg_color="transparent"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Clear button
        self.clear_btn = ctk.CTkButton(
            self,
            text=HIST_CLEAR,
            width=HISTORY_PANEL_WIDTH - 20,
            height=32,
            command=self._on_clear
        )
        self.clear_btn.pack(pady=10, padx=10)

        # Empty state label (shown when no history)
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text=HIST_EMPTY,
            font=("Arial", FONT_HISTORY_ENTRY),
            text_color="gray"
        )
        self.empty_label.pack(pady=20)

    def set_recall_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for when history entry is clicked."""
        self._recall_callback = callback

    def set_clear_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for when clear button is clicked."""
        self._clear_callback = callback

    def add_entry(self, expression: str, result: str) -> None:
        """Add a new calculation entry to the history.

        Args:
            expression: The expression that was evaluated
            result: The result of the evaluation
        """
        # Remove empty state on first entry
        if self.empty_label.winfo_exists():
            self.empty_label.pack_forget()

        # Create entry frame
        entry_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        entry_frame.pack(fill="x", pady=2)

        # Create clickable label with expression = result
        entry_text = f"{expression} = {result}"
        entry_label = ctk.CTkLabel(
            entry_frame,
            text=entry_text,
            font=("Arial", FONT_HISTORY_ENTRY),
            anchor="w",
            cursor="hand2"
        )
        entry_label.pack(fill="x", padx=5, pady=2)

        # Bind click event with lambda closure to capture result
        entry_label.bind("<Button-1>", lambda e, r=result: self._on_entry_click(r))

        # Track widget for clearing
        self._entry_widgets.append(entry_frame)

    def _on_entry_click(self, result: str) -> None:
        """Handle click on history entry."""
        if self._recall_callback:
            self._recall_callback(result)

    def _on_clear(self) -> None:
        """Handle clear button click."""
        self.clear_history()
        if self._clear_callback:
            self._clear_callback()

    def clear_history(self) -> None:
        """Clear all history entries and show empty state."""
        # Destroy all entry widgets
        for widget in self._entry_widgets:
            widget.destroy()
        self._entry_widgets.clear()

        # Show empty state
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text=HIST_EMPTY,
            font=("Arial", FONT_HISTORY_ENTRY),
            text_color="gray"
        )
        self.empty_label.pack(pady=20)
