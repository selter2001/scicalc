"""
MVC Controller connecting UI events to CalculatorEngine operations.
"""

import customtkinter as ctk
from src.calculator.logic.calculator import CalculatorEngine
from src.calculator.ui.calculator_window import CalculatorWindow


# Label-to-token mapping for button transformations
LABEL_TO_TOKEN = {
    "sin": "sin(",
    "cos": "cos(",
    "tan": "tan(",
    "\u221a": "sqrt(",  # √ symbol
    "log": "log(",
    "ln": "ln(",
    "x^y": "^",
    "n!": "factorial(",
    "\u03c0": "pi",  # π symbol
    "e": "e",
}


class CalculatorController:
    """
    Controller mediating between CalculatorWindow (view) and CalculatorEngine (model).
    Handles button clicks, expression building, and display updates.
    """

    def __init__(self, engine=None, view=None):
        """
        Initialize controller with optional engine and view for testing.

        Args:
            engine: CalculatorEngine instance (or mock for testing)
            view: CalculatorWindow instance (or mock for testing)
        """
        # Set appearance before creating window
        if view is None:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")

        self.engine = engine or CalculatorEngine()
        self.view = view or CalculatorWindow()

        # State
        self.expression = ""
        self.last_result = "0"
        self.error_state = False

        # Wire up callbacks
        self.view.set_button_callback(self.on_button_click)
        self.view.set_mode_callback(self.on_mode_change)
        self.view.set_angle_mode_callback(self.on_angle_mode_change)

        # Initialize display
        self.view.update_expression("")
        self.view.update_result("0")

    def on_button_click(self, label):
        """Route button clicks to appropriate handlers."""
        if label == "=":
            self._calculate()
        elif label == "C":
            self._clear()
        elif label == "\u232b":  # backspace
            self._backspace()
        else:
            self._append(label)

    def on_mode_change(self, mode):
        """Handle mode changes (basic/scientific)."""
        # Mode change handled by view, no engine state needed yet
        pass

    def on_angle_mode_change(self, mode):
        """Handle angle mode change from DEG/RAD toggle."""
        self.engine.set_angle_mode(mode)

    def _append(self, label):
        """Append button label to expression."""
        # If in error state, clear before appending new input
        if self.error_state:
            self._clear()

        # Transform label to token if needed
        token = LABEL_TO_TOKEN.get(label, label)

        # Append to expression
        self.expression += token

        # Update display
        self.view.update_expression(self.expression)
        self.view.update_result(self.last_result)

    def _calculate(self):
        """Evaluate current expression."""
        if not self.expression:
            return  # Empty expression, do nothing

        # Call engine
        result = self.engine.calculate(self.expression)

        if result["success"]:
            # Update display with result
            self.last_result = result["result"]
            self.view.update_result(self.last_result)
            self.error_state = False
        else:
            # Show error
            self.view.update_result(result["error"])
            self.error_state = True

    def _clear(self):
        """Clear expression and reset display."""
        self.expression = ""
        self.last_result = "0"
        self.error_state = False

        self.view.update_expression("")
        self.view.update_result("0")

    def _backspace(self):
        """Remove last character from expression."""
        if self.expression:
            self.expression = self.expression[:-1]
            self.view.update_expression(self.expression)

    def run(self):
        """Start the GUI main loop."""
        self.view.mainloop()
