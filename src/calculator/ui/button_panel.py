"""
Button panel for calculator with basic and scientific layouts.
"""

import customtkinter as ctk
from src.calculator.config.constants import (
    BASIC_LAYOUT,
    SCIENTIFIC_ROW_1,
    SCIENTIFIC_ROW_2,
    SCIENTIFIC_ROW_3,
    BUTTON_COLORS,
    BUTTON_CORNER_RADIUS,
    BUTTON_PADDING,
    FONT_BUTTON
)


class ButtonPanel(ctk.CTkFrame):
    """
    Grid of calculator buttons with basic and scientific layouts.
    Supports mode switching and responsive resizing.
    """

    def __init__(self, master):
        super().__init__(master)

        self.callback = None
        self.mode = "basic"
        self.buttons = {}

        self._create_buttons()
        self._configure_grid()

    def _create_buttons(self):
        """Create all buttons for basic and scientific modes."""
        # Basic layout (always visible)
        for row_idx, row in enumerate(BASIC_LAYOUT):
            for col_idx, label in enumerate(row):
                btn = self._create_button(label, row_idx, col_idx)
                self.buttons[f"basic_{row_idx}_{col_idx}"] = btn

        # Scientific rows (hidden initially)
        for row_idx, label in enumerate(SCIENTIFIC_ROW_1):
            btn = self._create_button(label, row_idx, col_idx=row_idx)
            btn.grid_remove()  # Hide initially
            self.buttons[f"sci1_{row_idx}"] = btn

        for row_idx, label in enumerate(SCIENTIFIC_ROW_2):
            btn = self._create_button(label, row_idx + 1, col_idx=row_idx)
            btn.grid_remove()
            self.buttons[f"sci2_{row_idx}"] = btn

        for row_idx, label in enumerate(SCIENTIFIC_ROW_3):
            btn = self._create_button(label, row_idx + 2, col_idx=row_idx)
            btn.grid_remove()
            self.buttons[f"sci3_{row_idx}"] = btn

    def _create_button(self, label, row, col):
        """Create a single button with appropriate styling."""
        # Determine button type for coloring
        button_type = self._get_button_type(label)
        colors = BUTTON_COLORS[button_type]

        # Use lambda with default argument to capture label value
        btn = ctk.CTkButton(
            self,
            text=label,
            command=lambda l=label: self._on_click(l),
            font=("Arial", FONT_BUTTON),
            corner_radius=BUTTON_CORNER_RADIUS,
            fg_color=colors["fg_color"],
            hover_color=colors["hover_color"],
            text_color=colors["text_color"]
        )

        btn.grid(
            row=row,
            column=col,
            padx=BUTTON_PADDING,
            pady=BUTTON_PADDING,
            sticky="nsew"
        )

        return btn

    def _get_button_type(self, label):
        """Determine button type for color coding."""
        if label in "0123456789":
            return "number"
        elif label in "+-*/":
            return "operator"
        elif label == "=":
            return "equals"
        elif label in ["C", "\u232b"]:
            return "action"
        else:
            return "function"

    def _on_click(self, label):
        """Handle button click by calling registered callback."""
        if self.callback:
            self.callback(label)

    def _configure_grid(self):
        """Configure grid weights for responsive resizing."""
        # Basic mode: 5 rows x 4 columns
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def set_callback(self, callback):
        """Set callback function for button clicks."""
        self.callback = callback

    def set_mode(self, mode):
        """Switch between basic and scientific modes."""
        self.mode = mode

        if mode == "scientific":
            # Show scientific rows above basic layout
            # Shift basic layout down by 3 rows
            for row_idx, row in enumerate(BASIC_LAYOUT):
                for col_idx, label in enumerate(row):
                    key = f"basic_{row_idx}_{col_idx}"
                    self.buttons[key].grid(row=row_idx + 3, column=col_idx)

            # Show scientific buttons
            for row_idx, label in enumerate(SCIENTIFIC_ROW_1):
                self.buttons[f"sci1_{row_idx}"].grid(row=0, column=row_idx)
            for row_idx, label in enumerate(SCIENTIFIC_ROW_2):
                self.buttons[f"sci2_{row_idx}"].grid(row=1, column=row_idx)
            for row_idx, label in enumerate(SCIENTIFIC_ROW_3):
                self.buttons[f"sci3_{row_idx}"].grid(row=2, column=row_idx)

            # Configure additional rows for scientific mode
            for i in range(3):
                self.grid_rowconfigure(i, weight=1)

        else:  # basic mode
            # Hide scientific buttons
            for key in list(self.buttons.keys()):
                if key.startswith("sci"):
                    self.buttons[key].grid_remove()

            # Reset basic layout to original positions
            for row_idx, row in enumerate(BASIC_LAYOUT):
                for col_idx, label in enumerate(row):
                    key = f"basic_{row_idx}_{col_idx}"
                    self.buttons[key].grid(row=row_idx, column=col_idx)
