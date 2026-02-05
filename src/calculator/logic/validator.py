"""
InputValidator - validates calculator input expressions.
Checks parentheses balance, syntax, and returns Polish error messages.
"""
import re
from src.calculator.config.locale import (
    ERROR_EMPTY_EXPRESSION,
    ERROR_UNBALANCED_PARENTHESES,
    ERROR_MISSING_CLOSING_PARENTHESIS,
    ERROR_MISSING_OPENING_PARENTHESIS,
    ERROR_INVALID_EXPRESSION
)


class InputValidator:
    """
    Validates calculator input expressions.

    Checks:
    - Empty expressions
    - Balanced parentheses with position tracking
    - Basic syntax validation
    """

    def __init__(self):
        """Initialize the validator."""
        pass

    def validate(self, expression: str) -> dict:
        """
        Validate an expression.

        Args:
            expression: The expression string to validate

        Returns:
            dict with keys:
                - valid (bool): True if valid, False otherwise
                - error (str): Error message if invalid, None if valid
                - position (int): Position of error if applicable, None otherwise
        """
        # Strip whitespace
        expr = expression.strip()

        # Check for empty expression
        if not expr:
            return {
                "valid": False,
                "error": ERROR_EMPTY_EXPRESSION,
                "position": None
            }

        # Validate parentheses
        paren_result = self._validate_parentheses(expr)
        if not paren_result["valid"]:
            return paren_result

        # Validate syntax
        syntax_result = self._validate_syntax(expr)
        if not syntax_result["valid"]:
            return syntax_result

        # All validations passed
        return {
            "valid": True,
            "error": None,
            "position": None
        }

    def _validate_parentheses(self, expression: str) -> dict:
        """
        Validate parentheses balance using stack-based matching.

        Args:
            expression: The expression to check

        Returns:
            dict with valid, error, position keys
        """
        stack = []

        for i, char in enumerate(expression):
            if char == '(':
                stack.append(i)
            elif char == ')':
                if not stack:
                    # Extra closing parenthesis
                    return {
                        "valid": False,
                        "error": ERROR_MISSING_OPENING_PARENTHESIS.format(i),
                        "position": i
                    }
                stack.pop()

        # Check for unclosed parentheses
        if stack:
            position = stack[-1]
            return {
                "valid": False,
                "error": ERROR_MISSING_CLOSING_PARENTHESIS,
                "position": position
            }

        return {
            "valid": True,
            "error": None,
            "position": None
        }

    def _validate_syntax(self, expression: str) -> dict:
        """
        Validate basic syntax rules.

        Checks for:
        - Consecutive operators (except unary minus)
        - Trailing operators
        - Invalid characters

        Args:
            expression: The expression to check

        Returns:
            dict with valid, error, position keys
        """
        # Allow: digits, operators, parentheses, decimal point, whitespace
        valid_chars = re.compile(r'^[\d+\-*/().eE\s]+$')
        if not valid_chars.match(expression):
            return {
                "valid": False,
                "error": ERROR_INVALID_EXPRESSION,
                "position": None
            }

        # Remove whitespace for operator checking
        expr_no_space = expression.replace(' ', '')

        # Check for trailing operators
        if expr_no_space and expr_no_space[-1] in '+-*/':
            return {
                "valid": False,
                "error": ERROR_INVALID_EXPRESSION,
                "position": len(expr_no_space) - 1
            }

        # Check for consecutive operators (excluding unary minus)
        operators = ['+', '-', '*', '/']
        for i in range(len(expr_no_space) - 1):
            current = expr_no_space[i]
            next_char = expr_no_space[i + 1]

            # Check if we have two operators in a row
            if current in operators and next_char in operators:
                # Allow unary minus after operators or at start
                if next_char == '-' and (i == 0 or current in operators or expr_no_space[i] == '('):
                    continue
                # Allow unary minus after opening parenthesis
                if current == '(' and next_char == '-':
                    continue
                # Otherwise, it's invalid
                return {
                    "valid": False,
                    "error": ERROR_INVALID_EXPRESSION,
                    "position": i + 1
                }

        return {
            "valid": True,
            "error": None,
            "position": None
        }
