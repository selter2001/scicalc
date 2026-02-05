"""
Centralized Polish UI strings for SciCalc.
All user-facing messages in Polish with proper diacritics.
"""

# Welcome and interface
MSG_WELCOME = "Witamy w SciCalc - Kalkulatorze Naukowym"
MSG_PROMPT = "Wprowadź wyrażenie (lub 'quit' aby wyjść): "
MSG_GOODBYE = "Do widzenia!"

# Error messages
ERROR_DIVISION_BY_ZERO = "Nie można dzielić przez zero"
ERROR_INVALID_EXPRESSION = "Błąd: Nieprawidłowe wyrażenie"
ERROR_SYNTAX_ERROR = "Błąd: Błąd składni"
ERROR_UNDEFINED_FUNCTION = "Błąd: Niezdefiniowana funkcja"
ERROR_UNDEFINED_VARIABLE = "Błąd: Niezdefiniowana zmienna"
ERROR_MATH_DOMAIN = "Błąd: Wartość poza dziedziną funkcji"
ERROR_OVERFLOW = "Błąd: Wynik zbyt duży"
ERROR_INVALID_ANGLE_MODE = "Błąd: Nieprawidłowy tryb kątów"
ERROR_EXPRESSION_TOO_LONG = "Błąd: Wyrażenie zbyt długie"
ERROR_EMPTY_EXPRESSION = "Wyrażenie jest puste"
ERROR_UNBALANCED_PARENTHESES = "Niezrównoważone nawiasy na pozycji {}"
ERROR_MISSING_CLOSING_PARENTHESIS = "Brak zamykającego nawiasu"
ERROR_MISSING_OPENING_PARENTHESIS = "Brak otwierającego nawiasu na pozycji {}"

# Factorial errors
ERROR_FACTORIAL_NOT_INTEGER = "Silnia wymaga liczby całkowitej"
ERROR_FACTORIAL_NEGATIVE = "Silnia nie jest zdefiniowana dla liczb ujemnych"
ERROR_FACTORIAL_TOO_LARGE = "Silnia: liczba zbyt duża (max 170)"

# Info messages
INFO_RESULT = "Wynik: {}"
INFO_ANGLE_MODE_CHANGED = "Tryb kątów zmieniony na: {}"
INFO_MEMORY_STORED = "Zapisano do pamięci: {}"
INFO_MEMORY_RECALLED = "Przywołano z pamięci: {}"
INFO_MEMORY_CLEARED = "Pamięć wyczyszczona"

# Help messages
HELP_USAGE = """
Użycie:
  - Wprowadź wyrażenie matematyczne
  - Użyj funkcji: sin(), cos(), tan(), sqrt(), log(), ln()
  - Stałe: pi, e
  - Operatory: +, -, *, /, ^, %
  - quit - wyjście z programu
"""

# Angle mode
ANGLE_MODE_DEGREES = "stopnie"
ANGLE_MODE_RADIANS = "radiany"
ANGLE_MODE_GRADIANS = "gradiany"

# Window
WINDOW_TITLE = "SciCalc - Kalkulator Naukowy"

# Button labels (Polish where applicable)
BTN_CLEAR = "C"
BTN_BACKSPACE = "\u232b"
BTN_EQUALS = "="
BTN_DECIMAL = "."
BTN_OPEN_PAREN = "("
BTN_CLOSE_PAREN = ")"
BTN_POWER = "x^y"
BTN_FACTORIAL = "n!"
BTN_SQRT = "\u221a"
BTN_NEGATE = "+/-"

# Mode labels
BTN_MODE_BASIC = "Podstawowy"
BTN_MODE_SCIENTIFIC = "Naukowy"

# Angle mode labels (display)
ANGLE_DEG = "DEG"
ANGLE_RAD = "RAD"

# History panel
HIST_TITLE = "Historia"
HIST_CLEAR = "Wyczysc historie"
HIST_EMPTY = "Brak historii"
