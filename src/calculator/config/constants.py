"""
Calculator configuration constants.
"""

from decimal import ROUND_HALF_UP

# Precision settings
DECIMAL_PRECISION = 28  # Decimal arithmetic precision
DECIMAL_ROUNDING = ROUND_HALF_UP  # Rounding mode
DISPLAY_PRECISION = 10  # Number of digits to display

# Supported operators
OPERATORS = {
    '+': 'addition',
    '-': 'subtraction',
    '*': 'multiplication',
    '/': 'division',
    '^': 'power',
    '%': 'modulo',
}

# Expression limits
MAX_EXPRESSION_LENGTH = 1000  # Maximum input length
MAX_RECURSION_DEPTH = 100  # Maximum function nesting depth

# Angle modes
ANGLE_MODE_DEGREES = 'degrees'
ANGLE_MODE_RADIANS = 'radians'
ANGLE_MODE_GRADIANS = 'gradians'
DEFAULT_ANGLE_MODE = ANGLE_MODE_DEGREES

# Mathematical constants (used by simpleeval)
MATH_CONSTANTS = {
    'pi': 3.141592653589793,
    'e': 2.718281828459045,
}

# Function categories for validation
BASIC_FUNCTIONS = ['sin', 'cos', 'tan', 'sqrt', 'log', 'ln', 'abs', 'factorial']
ADVANCED_FUNCTIONS = ['asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh']
ALL_FUNCTIONS = BASIC_FUNCTIONS + ADVANCED_FUNCTIONS

# Factorial limits
MAX_FACTORIAL_INPUT = 170  # math.factorial(171) overflows float
