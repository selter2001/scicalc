"""
SafeEvaluator - safely evaluates mathematical expressions using simpleeval.
Converts results to Decimal for precision arithmetic.
Supports scientific functions with angle mode and power operator.
"""
import ast
import math
import operator
from decimal import Decimal
from simpleeval import SimpleEval, DEFAULT_FUNCTIONS, InvalidExpression, NameNotDefined
from src.calculator.config.locale import (
    ERROR_DIVISION_BY_ZERO,
    ERROR_INVALID_EXPRESSION,
    ERROR_UNDEFINED_FUNCTION,
    ERROR_UNDEFINED_VARIABLE,
    ERROR_FACTORIAL_NOT_INTEGER,
    ERROR_FACTORIAL_NEGATIVE,
    ERROR_FACTORIAL_TOO_LARGE,
    ERROR_MATH_DOMAIN,
    ERROR_OVERFLOW
)
from src.calculator.config.constants import (
    DEFAULT_ANGLE_MODE,
    ANGLE_MODE_DEGREES,
    ANGLE_MODE_RADIANS,
    ANGLE_MODE_GRADIANS,
    MATH_CONSTANTS,
    MAX_FACTORIAL_INPUT
)


class SafeEvaluator:
    """
    Safely evaluates mathematical expressions using simpleeval.

    Features:
    - No eval() - uses simpleeval for security
    - Scientific functions (sin, cos, tan, sqrt, log, ln, factorial)
    - Angle mode support (degrees/radians/gradians)
    - Power operator (^) remapped from XOR
    - Mathematical constants (pi, e)
    - Converts float results to Decimal for precision
    - Returns Polish error messages
    """

    def __init__(self):
        """Initialize the evaluator with default angle mode."""
        self.angle_mode = DEFAULT_ANGLE_MODE
        self.functions = self._build_functions()
        self.names = self._build_names()
        self._evaluator = self._build_evaluator()

    def _build_functions(self) -> dict:
        """
        Build the function dictionary for simpleeval.

        Returns:
            dict: Function name -> function mapping
        """
        # Start with simpleeval's default safe functions
        functions = DEFAULT_FUNCTIONS.copy()

        # Add angle-aware trigonometric functions
        functions.update({
            'sin': lambda x: math.sin(self._to_radians(x)),
            'cos': lambda x: math.cos(self._to_radians(x)),
            'tan': lambda x: math.tan(self._to_radians(x)),
        })

        # Add other mathematical functions
        functions.update({
            'sqrt': math.sqrt,
            'log': math.log10,  # log(x) is base-10
            'ln': math.log,     # ln(x) is natural log
            'abs': abs,
            'factorial': self._safe_factorial,
        })

        return functions

    def _build_names(self) -> dict:
        """
        Build the names dictionary for mathematical constants.

        Returns:
            dict: Constant name -> value mapping
        """
        return MATH_CONSTANTS.copy()

    def _build_evaluator(self) -> SimpleEval:
        """
        Build a SimpleEval instance with operator remapping.

        Returns:
            SimpleEval: Configured evaluator instance
        """
        evaluator = SimpleEval()
        evaluator.functions = self.functions
        evaluator.names = self.names

        # Remap ^ from XOR to power
        # simpleeval uses AST node types as keys
        # ^ is BitXor in AST, we need to map it to power operator
        evaluator.operators[ast.BitXor] = operator.pow

        return evaluator

    def _to_radians(self, angle: float) -> float:
        """
        Convert angle to radians based on current angle mode.

        Args:
            angle: Angle value in current mode

        Returns:
            float: Angle in radians
        """
        if self.angle_mode == ANGLE_MODE_DEGREES:
            return math.radians(angle)
        elif self.angle_mode == ANGLE_MODE_GRADIANS:
            # 1 gradian = pi/200 radians
            return angle * (math.pi / 200)
        else:  # ANGLE_MODE_RADIANS
            return angle

    def _safe_factorial(self, n: float) -> int:
        """
        Safely compute factorial with validation.

        Args:
            n: Input number

        Returns:
            int: Factorial result

        Raises:
            ValueError: If n is not a non-negative integer
            OverflowError: If n is too large
        """
        # Check if n is an integer
        if not isinstance(n, int) and (not isinstance(n, float) or not n.is_integer()):
            raise ValueError(ERROR_FACTORIAL_NOT_INTEGER)

        # Convert to int
        n_int = int(n)

        # Check if non-negative
        if n_int < 0:
            raise ValueError(ERROR_FACTORIAL_NEGATIVE)

        # Check if within bounds
        if n_int > MAX_FACTORIAL_INPUT:
            raise OverflowError(ERROR_FACTORIAL_TOO_LARGE)

        # Compute factorial
        return math.factorial(n_int)

    def set_angle_mode(self, mode: str) -> None:
        """
        Set the angle mode for trigonometric functions.

        Args:
            mode: Angle mode (degrees/radians/gradians)
        """
        self.angle_mode = mode
        # Rebuild functions to capture new angle mode
        self.functions = self._build_functions()
        self._evaluator = self._build_evaluator()

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
            # Use SimpleEval for safe evaluation
            # This prevents code injection and limits to mathematical operations
            result = self._evaluator.eval(expression)

            # Convert to Decimal for precision
            # simpleeval uses float internally, so we need to convert
            # Handle both int and float results
            if isinstance(result, int):
                # Direct conversion for integers (no precision loss)
                decimal_result = Decimal(result)
            else:
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

        except ValueError as e:
            # Math domain errors or factorial validation errors
            # Check if it's one of our custom error messages
            error_msg = str(e)
            if error_msg in [ERROR_FACTORIAL_NOT_INTEGER, ERROR_FACTORIAL_NEGATIVE]:
                return {
                    "success": False,
                    "result": None,
                    "error": error_msg
                }
            else:
                # Math domain error (e.g., sqrt of negative number)
                return {
                    "success": False,
                    "result": None,
                    "error": ERROR_MATH_DOMAIN
                }

        except OverflowError as e:
            # Overflow errors (factorial too large, etc.)
            error_msg = str(e)
            if error_msg == ERROR_FACTORIAL_TOO_LARGE:
                return {
                    "success": False,
                    "result": None,
                    "error": error_msg
                }
            else:
                return {
                    "success": False,
                    "result": None,
                    "error": ERROR_OVERFLOW
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
