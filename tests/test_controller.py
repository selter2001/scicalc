"""
Unit tests for CalculatorController with mocked view.
"""

import pytest
from unittest.mock import Mock
from src.calculator.controller.calculator_controller import CalculatorController
from src.calculator.logic.calculator import CalculatorEngine


@pytest.fixture
def mock_view():
    """Create a mock view for testing."""
    view = Mock()
    view.update_expression = Mock()
    view.update_result = Mock()
    view.set_button_callback = Mock()
    view.set_mode_callback = Mock()
    view.set_angle_mode_callback = Mock()
    view.set_history_recall_callback = Mock()
    view.set_history_clear_callback = Mock()
    view.add_history_entry = Mock()
    view.clear_history = Mock()
    view.get_result = Mock(return_value="42")
    view.mainloop = Mock()
    return view


@pytest.fixture
def controller(mock_view):
    """Create controller with real engine and mock view."""
    engine = CalculatorEngine()
    return CalculatorController(engine=engine, view=mock_view)


def test_digit_appends_to_expression(controller, mock_view):
    """Test that clicking a digit appends to expression."""
    controller.on_button_click("5")
    mock_view.update_expression.assert_called_with("5")


def test_multiple_digits(controller, mock_view):
    """Test building multi-digit numbers."""
    controller.on_button_click("1")
    controller.on_button_click("2")
    controller.on_button_click("3")
    mock_view.update_expression.assert_called_with("123")
    assert controller.expression == "123"


def test_operator_appends(controller, mock_view):
    """Test that operators append correctly."""
    controller.on_button_click("5")
    controller.on_button_click("+")
    controller.on_button_click("3")
    mock_view.update_expression.assert_called_with("5+3")


def test_equals_calculates(controller, mock_view):
    """Test that equals button evaluates expression."""
    controller.on_button_click("2")
    controller.on_button_click("+")
    controller.on_button_click("3")
    controller.on_button_click("=")
    mock_view.update_result.assert_called_with("5")


def test_equals_error(controller, mock_view):
    """Test that invalid expression shows error."""
    controller.on_button_click("5")
    controller.on_button_click("/")
    controller.on_button_click("0")
    controller.on_button_click("=")
    # Should show error message
    last_call = mock_view.update_result.call_args[0][0]
    assert "Błąd" in last_call or "zero" in last_call


def test_clear_resets(controller, mock_view):
    """Test that C button clears everything."""
    controller.on_button_click("5")
    controller.on_button_click("+")
    controller.on_button_click("3")
    controller.on_button_click("C")
    mock_view.update_expression.assert_called_with("")
    mock_view.update_result.assert_called_with("0")
    assert controller.expression == ""


def test_backspace_removes_last(controller, mock_view):
    """Test that backspace removes last character."""
    controller.on_button_click("1")
    controller.on_button_click("2")
    controller.on_button_click("3")
    controller.on_button_click("\u232b")  # backspace
    mock_view.update_expression.assert_called_with("12")


def test_sin_button_appends_function(controller, mock_view):
    """Test that sin button appends 'sin(' to expression."""
    controller.on_button_click("sin")
    mock_view.update_expression.assert_called_with("sin(")


def test_sqrt_button_maps_to_function(controller, mock_view):
    """Test that √ symbol maps to sqrt( function."""
    controller.on_button_click("\u221a")  # √
    mock_view.update_expression.assert_called_with("sqrt(")


def test_power_button_maps_to_caret(controller, mock_view):
    """Test that x^y button maps to ^ operator."""
    controller.on_button_click("2")
    controller.on_button_click("x^y")
    controller.on_button_click("3")
    mock_view.update_expression.assert_called_with("2^3")


def test_factorial_button_maps_to_function(controller, mock_view):
    """Test that n! button maps to factorial( function."""
    controller.on_button_click("n!")
    mock_view.update_expression.assert_called_with("factorial(")


def test_pi_button_maps_to_constant(controller, mock_view):
    """Test that π symbol maps to pi constant."""
    controller.on_button_click("\u03c0")  # π
    mock_view.update_expression.assert_called_with("pi")


def test_empty_equals_does_nothing(controller, mock_view):
    """Test that equals on empty expression does nothing."""
    mock_view.reset_mock()
    controller.on_button_click("=")
    # Should not update result (stays at initial "0")
    # The last call should be from initialization, not from equals
    assert mock_view.update_result.call_count == 0


def test_error_then_digit_clears(controller, mock_view):
    """Test that typing after error clears error state."""
    # Create error
    controller.on_button_click("5")
    controller.on_button_click("/")
    controller.on_button_click("0")
    controller.on_button_click("=")
    assert controller.error_state is True

    # Type new digit should clear
    controller.on_button_click("7")
    assert controller.error_state is False
    mock_view.update_expression.assert_called_with("7")


def test_full_scientific_expression(controller, mock_view):
    """Test complete scientific calculation: sin(90)."""
    controller.on_button_click("sin")
    controller.on_button_click("9")
    controller.on_button_click("0")
    controller.on_button_click(")")
    controller.on_button_click("=")

    # sin(90 degrees) should be 1
    last_result_call = mock_view.update_result.call_args[0][0]
    assert last_result_call == "1"


# --- Angle mode tests ---

def test_angle_mode_change_to_radians(controller, mock_view):
    """Switching to RAD sets engine to radians mode."""
    controller.on_angle_mode_change("radians")
    controller.expression = "sin(pi/2)"
    controller.on_button_click("=")
    last_result = mock_view.update_result.call_args[0][0]
    assert last_result == "1"


def test_angle_mode_change_to_degrees(controller, mock_view):
    """Switching to DEG sets engine to degrees mode."""
    controller.on_angle_mode_change("degrees")
    controller.expression = "sin(30)"
    controller.on_button_click("=")
    last_result = mock_view.update_result.call_args[0][0]
    assert last_result == "0.5"


def test_angle_mode_deg_vs_rad_different_results(controller, mock_view):
    """Same expression gives different results in DEG vs RAD."""
    controller.on_angle_mode_change("degrees")
    controller.expression = "sin(30)"
    controller.on_button_click("=")
    deg_result = mock_view.update_result.call_args[0][0]

    controller.on_angle_mode_change("radians")
    controller.expression = "sin(30)"
    controller.error_state = False
    controller.on_button_click("=")
    rad_result = mock_view.update_result.call_args[0][0]

    assert deg_result != rad_result
    assert deg_result == "0.5"


# --- Keyboard input tests ---

def test_keyboard_digit_input(controller, mock_view):
    """Keyboard digit is routed through on_button_click."""
    controller.on_button_click("7")
    assert controller.expression == "7"
    mock_view.update_expression.assert_called_with("7")


def test_keyboard_operator_input(controller, mock_view):
    """Keyboard operator is routed through on_button_click."""
    controller.on_button_click("5")
    controller.on_button_click("+")
    controller.on_button_click("3")
    assert controller.expression == "5+3"


def test_keyboard_enter_calculates(controller, mock_view):
    """Enter key (mapped to =) calculates expression."""
    controller.expression = "2+3"
    controller.on_button_click("=")
    mock_view.update_result.assert_called_with("5")


def test_keyboard_escape_clears(controller, mock_view):
    """Escape key (mapped to C) clears expression."""
    controller.expression = "123"
    controller.on_button_click("C")
    assert controller.expression == ""
    mock_view.update_expression.assert_called_with("")
    mock_view.update_result.assert_called_with("0")


def test_keyboard_backspace_deletes(controller, mock_view):
    """Backspace key removes last character."""
    controller.expression = "123"
    controller.on_button_click("\u232b")
    assert controller.expression == "12"


def test_keyboard_parentheses(controller, mock_view):
    """Keyboard parentheses work in expressions."""
    controller.on_button_click("(")
    controller.on_button_click("2")
    controller.on_button_click("+")
    controller.on_button_click("3")
    controller.on_button_click(")")
    controller.on_button_click("*")
    controller.on_button_click("4")
    assert controller.expression == "(2+3)*4"
    controller.on_button_click("=")
    mock_view.update_result.assert_called_with("20")


def test_paste_numeric_string(controller, mock_view):
    """Pasting a numeric string appends it to expression."""
    controller.on_button_click("3.14")
    assert controller.expression == "3.14"


# --- History tests ---

def test_history_added_on_calculate(controller, mock_view):
    """Successful calculation adds entry to history."""
    controller.on_button_click("2")
    controller.on_button_click("+")
    controller.on_button_click("3")
    controller.on_button_click("=")

    # Check history list
    assert len(controller.history) == 1
    assert controller.history[0] == ("2+3", "5")

    # Check view was updated
    mock_view.add_history_entry.assert_called_once_with("2+3", "5")


def test_history_not_added_on_error(controller, mock_view):
    """Failed calculation does not add to history."""
    controller.on_button_click("5")
    controller.on_button_click("/")
    controller.on_button_click("0")
    controller.on_button_click("=")

    # History should be empty
    assert len(controller.history) == 0
    mock_view.add_history_entry.assert_not_called()


def test_history_multiple_entries(controller, mock_view):
    """Multiple calculations create multiple history entries."""
    # First calculation
    controller.on_button_click("2")
    controller.on_button_click("+")
    controller.on_button_click("3")
    controller.on_button_click("=")

    # Clear and second calculation
    controller.on_button_click("C")
    controller.on_button_click("5")
    controller.on_button_click("*")
    controller.on_button_click("4")
    controller.on_button_click("=")

    # Check history has both
    assert len(controller.history) == 2
    assert controller.history[0] == ("2+3", "5")
    assert controller.history[1] == ("5*4", "20")
    assert mock_view.add_history_entry.call_count == 2


def test_history_recall_inserts_result(controller, mock_view):
    """Clicking history entry inserts result into expression."""
    controller.on_history_recall("42")
    assert controller.expression == "42"
    mock_view.update_expression.assert_called_with("42")


def test_history_recall_clears_error_first(controller, mock_view):
    """History recall clears error state before inserting."""
    # Create error state
    controller.on_button_click("5")
    controller.on_button_click("/")
    controller.on_button_click("0")
    controller.on_button_click("=")
    assert controller.error_state is True

    # Recall should clear error
    controller.on_history_recall("10")
    assert controller.error_state is False
    assert controller.expression == "10"


def test_history_max_limit(controller, mock_view):
    """History enforces MAX_HISTORY_ENTRIES limit."""
    from src.calculator.config.constants import MAX_HISTORY_ENTRIES

    # Add more than max entries
    for i in range(MAX_HISTORY_ENTRIES + 5):
        controller.expression = f"{i}+{i}"
        controller._calculate()

    # Should only keep last MAX_HISTORY_ENTRIES
    assert len(controller.history) == MAX_HISTORY_ENTRIES
    # First entry should be entry #5 (entries 0-4 were dropped)
    assert controller.history[0] == ("5+5", "10")


def test_history_cleared_by_controller(controller, mock_view):
    """Clear callback clears controller's history list."""
    # Add some history
    controller.on_button_click("2")
    controller.on_button_click("+")
    controller.on_button_click("3")
    controller.on_button_click("=")
    assert len(controller.history) == 1

    # Simulate clear button callback
    controller._on_history_cleared()
    assert len(controller.history) == 0
