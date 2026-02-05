"""
Display panel for calculator showing expression and result.
"""

import customtkinter as ctk
from src.calculator.config.constants import (
    FONT_EXPRESSION,
    FONT_RESULT,
    ANGLE_MODE_DEGREES,
    ANGLE_MODE_RADIANS
)
from src.calculator.config.locale import ANGLE_DEG, ANGLE_RAD


class DisplayPanel(ctk.CTkFrame):
    """
    Display panel with expression label (top) and result label (bottom).
    Uses StringVar for dynamic updates from controller.
    """

    def __init__(self, master):
        super().__init__(master)

        # StringVars for dynamic text updates
        self.expression_var = ctk.StringVar(value="")
        self.result_var = ctk.StringVar(value="0")

        # Callback for angle mode changes
        self.angle_mode_callback = None

        # Expression label (smaller, top)
        self.expression_label = ctk.CTkLabel(
            self,
            textvariable=self.expression_var,
            font=("Arial", FONT_EXPRESSION),
            anchor="e",
            justify="right"
        )
        self.expression_label.pack(fill="x", padx=10, pady=(10, 0))

        # Result label (larger, bottom)
        self.result_label = ctk.CTkLabel(
            self,
            textvariable=self.result_var,
            font=("Arial", FONT_RESULT, "bold"),
            anchor="e",
            justify="right"
        )
        self.result_label.pack(fill="x", padx=10, pady=(0, 10))

        # Angle mode selector (DEG/RAD toggle)
        self.angle_mode_selector = ctk.CTkSegmentedButton(
            self,
            values=[ANGLE_DEG, ANGLE_RAD],
            width=120,
            font=("Arial", 12),
            command=self._on_angle_mode_change
        )
        self.angle_mode_selector.set(ANGLE_DEG)
        self.angle_mode_selector.pack(anchor="w", padx=10, pady=(5, 5))

    def update_expression(self, text):
        """Update expression display."""
        self.expression_var.set(text)

    def update_result(self, text):
        """Update result display."""
        self.result_var.set(text)

    def set_angle_mode_callback(self, callback):
        """Set callback for angle mode changes."""
        self.angle_mode_callback = callback

    def _on_angle_mode_change(self, value):
        """Handle angle mode toggle change."""
        # Map display label to angle mode constant
        mode = ANGLE_MODE_DEGREES if value == ANGLE_DEG else ANGLE_MODE_RADIANS
        if self.angle_mode_callback:
            self.angle_mode_callback(mode)

    def get_result(self):
        """Get current result text for clipboard operations."""
        return self.result_var.get()
