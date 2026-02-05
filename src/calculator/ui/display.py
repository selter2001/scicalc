"""
Display panel for calculator showing expression and result.
"""

import customtkinter as ctk
from calculator.config.constants import FONT_EXPRESSION, FONT_RESULT


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

    def update_expression(self, text):
        """Update expression display."""
        self.expression_var.set(text)

    def update_result(self, text):
        """Update result display."""
        self.result_var.set(text)
