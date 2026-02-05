"""
SafeEvaluator - safely evaluates mathematical expressions using simpleeval.
Converts results to Decimal for precision arithmetic.
"""
from decimal import Decimal
from simpleeval import simple_eval, InvalidExpression, NameNotDefined
from src.calculator.config.locale import (
    ERROR_DIVISION_BY_ZERO,
    ERROR_INVALID_EXPRESSION,
    ERROR_UNDEFINED_FUNCTION,
    ERROR_UNDEFINED_VARIABLE
)


class SafeEvaluator:
    """
    Safely evaluates mathematical expressions using simpleeval.

    Features:
    - No eval() - uses simpleeval for security
    - Converts float results to Decimal for precision
    - Returns Polish error messages
    """

    def __init__(self):
        """Initialize the evaluator."""
        pass

    def evaluate(self, expression: str) -> dict:
        """
        Safely evaluate a mathematical expression.

        Args:
            expression: The expression string to evaluate

        Returns:
            dict with keys:
                - success (bool): True if evaluation succeeded
                - result (Decimal): The result if successful, None otherwise
                - error (str): Error message if failed, None if successful
        """
        try:
            # Use simpleeval's simple_eval for safe evaluation
            # This prevents code injection and limits to mathematical operations
            result = simple_eval(expression)

            # Convert to Decimal for precision
            # simpleeval uses float internally, so we need to convert
            # Use round(result, 10) to handle float precision issues before conversion
            decimal_result = Decimal(str(round(result, 10)))

            return {
                "success": True,
                "result": decimal_result,
                "error": None
            }

        except ZeroDivisionError:
            # Division by zero
            return {
                "success": False,
                "result": None,
                "error": ERROR_DIVISION_BY_ZERO
            }

        except (InvalidExpression, SyntaxError):
            # Invalid expression syntax
            return {
                "success": False,
                "result": None,
                "error": ERROR_INVALID_EXPRESSION
            }

        except NameNotDefined:
            # Undefined variable or function
            return {
                "success": False,
                "result": None,
                "error": ERROR_UNDEFINED_VARIABLE
            }

        except AttributeError:
            # Attribute access blocked (security)
            return {
                "success": False,
                "result": None,
                "error": ERROR_INVALID_EXPRESSION
            }

        except Exception as e:
            # Catch-all for other errors
            return {
                "success": False,
                "result": None,
                "error": ERROR_INVALID_EXPRESSION
            }
