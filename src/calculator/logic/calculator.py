"""
CalculatorEngine - orchestrates validation and evaluation.
Main calculator engine with Decimal precision and formatted output.
"""
from decimal import Decimal, getcontext, ROUND_HALF_UP
from src.calculator.logic.validator import InputValidator
from src.calculator.logic.evaluator import SafeEvaluator


class CalculatorEngine:
    """
    Main calculator engine orchestrating validator and evaluator.

    Features:
    - Input validation before evaluation
    - Decimal precision (28 digits, ROUND_HALF_UP)
    - Formatted string output with normalize()
    - Polish error messages
    """

    def __init__(self):
        """Initialize the calculator engine with Decimal context."""
        # Set up Decimal context for precision arithmetic
        context = getcontext()
        context.prec = 28  # 28 digits of precision
        context.rounding = ROUND_HALF_UP  # Financial rounding

        # Initialize validator and evaluator
        self.validator = InputValidator()
        self.evaluator = SafeEvaluator()

    def set_angle_mode(self, mode: str) -> None:
        """
        Set the angle mode for trigonometric functions.

        Args:
            mode: Angle mode (degrees/radians/gradians)
        """
        self.evaluator.set_angle_mode(mode)

    def calculate(self, expression: str) -> dict:
        """
        Calculate the result of a mathematical expression.

        Process:
        1. Validate input (parentheses, syntax)
        2. If valid, evaluate expression
        3. Format result as normalized string (no trailing zeros)

        Args:
            expression: The expression string to calculate

        Returns:
            dict with keys:
                - success (bool): True if calculation succeeded
                - result (str): Formatted result string if successful
                - error (str): Error message if failed
        """
        # Step 1: Validate input
        validation = self.validator.validate(expression)

        if not validation["valid"]:
            # Validation failed - return error
            return {
                "success": False,
                "result": None,
                "error": validation["error"]
            }

        # Step 2: Evaluate expression
        evaluation = self.evaluator.evaluate(expression)

        if not evaluation["success"]:
            # Evaluation failed - return error
            return {
                "success": False,
                "result": None,
                "error": evaluation["error"]
            }

        # Step 3: Format result
        decimal_result = evaluation["result"]

        # Use normalize() to remove trailing zeros
        # e.g., Decimal("3.00") -> Decimal("3")
        #       Decimal("0.30") -> Decimal("0.3")
        normalized = decimal_result.normalize()

        # Convert to string, avoiding scientific notation
        result_string = str(normalized)

        # Check if normalized used scientific notation (e.g., "2E+1")
        if 'E' in result_string or 'e' in result_string:
            # Format without scientific notation
            # Use a large number of decimal places, then strip trailing zeros
            result_string = format(normalized, '.20f')
            # Only strip trailing zeros after decimal point
            if '.' in result_string:
                result_string = result_string.rstrip('0').rstrip('.')
            else:
                result_string = result_string

        return {
            "success": True,
            "result": result_string,
            "error": None
        }
