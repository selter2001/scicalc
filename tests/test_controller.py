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
