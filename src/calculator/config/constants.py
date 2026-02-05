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

# UI Constants
WINDOW_MIN_WIDTH = 380
WINDOW_MIN_HEIGHT = 520
WINDOW_DEFAULT_GEOMETRY = "400x600"

# Font sizes
FONT_EXPRESSION = 16
FONT_RESULT = 32
FONT_BUTTON = 18

# Button styling
BUTTON_CORNER_RADIUS = 10
BUTTON_PADDING = 4

# Keyboard characters that map directly to expression tokens
KEYBOARD_CHARS = "0123456789+-*/()."

# Button layout for basic mode (5 rows x 4 columns)
BASIC_LAYOUT = [
    ["C", "\u232b", "(", ")"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
]

# Additional rows for scientific mode
SCIENTIFIC_ROW_1 = ["sin", "cos", "tan", "\u221a"]
SCIENTIFIC_ROW_2 = ["log", "ln", "x^y", "n!"]
SCIENTIFIC_ROW_3 = ["\u03c0", "e", "(", ")"]

# Color scheme for button types
BUTTON_COLORS = {
    "number": {"fg_color": "#2B2B2B", "hover_color": "#3B3B3B", "text_color": "white"},
    "operator": {"fg_color": "#FF9500", "hover_color": "#FFB340", "text_color": "white"},
    "function": {"fg_color": "#505050", "hover_color": "#606060", "text_color": "white"},
    "action": {"fg_color": "#D4D4D2", "hover_color": "#E4E4E2", "text_color": "black"},
    "equals": {"fg_color": "#FF9500", "hover_color": "#FFB340", "text_color": "white"},
}
