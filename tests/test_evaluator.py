"""
Tests for SafeEvaluator module.
Tests safe expression evaluation with simpleeval, Decimal conversion, and error handling.
"""
import pytest
from decimal import Decimal
from src.calculator.logic.evaluator import SafeEvaluator


class TestSafeEvaluator:
    """Test suite for SafeEvaluator class."""

    def setup_method(self):
        """Initialize evaluator before each test."""
        self.evaluator = SafeEvaluator()

    # Basic arithmetic tests
    def test_addition(self):
        """Test basic addition."""
        result = self.evaluator.evaluate("2+3")
        assert result["success"] is True
        assert result["result"] == Decimal("5")

    def test_subtraction(self):
        """Test basic subtraction."""
        result = self.evaluator.evaluate("10-4")
        assert result["success"] is True
        assert result["result"] == Decimal("6")

    def test_multiplication(self):
        """Test basic multiplication."""
        result = self.evaluator.evaluate("3*7")
        assert result["success"] is True
        assert result["result"] == Decimal("21")

    def test_division(self):
        """Test basic division."""
        result = self.evaluator.evaluate("8/2")
        assert result["success"] is True
        assert result["result"] == Decimal("4")

    # Decimal precision tests
    def test_decimal_precision_addition(self):
        """Test Decimal precision: 0.1+0.2 must equal exactly 0.3."""
        result = self.evaluator.evaluate("0.1+0.2")
        assert result["success"] is True
        assert result["result"] == Decimal("0.3")
        # String representation must be exact
        assert str(result["result"]) == "0.3"

    def test_decimal_precision_complex(self):
        """Test Decimal precision with complex calculation."""
        result = self.evaluator.evaluate("0.1+0.1+0.1")
        assert result["success"] is True
        assert result["result"] == Decimal("0.3")

    # Parentheses tests
    def test_simple_parentheses(self):
        """Test simple parentheses: (2+3)*4."""
        result = self.evaluator.evaluate("(2+3)*4")
        assert result["success"] is True
        assert result["result"] == Decimal("20")

    def test_nested_parentheses(self):
        """Test nested parentheses: ((1+2)*(3+4))."""
        result = self.evaluator.evaluate("((1+2)*(3+4))")
        assert result["success"] is True
        assert result["result"] == Decimal("21")

    def test_multiple_parentheses_groups(self):
        """Test multiple parentheses groups."""
        result = self.evaluator.evaluate("(2+3)*(4-1)")
        assert result["success"] is True
        assert result["result"] == Decimal("15")

    # Division by zero tests
    def test_division_by_zero_simple(self):
        """Test division by zero shows Polish error."""
        result = self.evaluator.evaluate("5/0")
        assert result["success"] is False
        assert "nie można" in result["error"].lower() or "nie mozna" in result["error"].lower()
        assert "zero" in result["error"].lower()

    def test_division_by_zero_complex(self):
        """Test division by zero in complex expression."""
        result = self.evaluator.evaluate("10/(5-5)")
        assert result["success"] is False
        assert "zero" in result["error"].lower()

    # Security tests (no eval() - using simpleeval)
    def test_no_dangerous_code_execution(self):
        """Test that dangerous code cannot be executed."""
        result = self.evaluator.evaluate("__import__('os').system('ls')")
        assert result["success"] is False

    def test_no_attribute_access(self):
        """Test that attribute access is blocked."""
        result = self.evaluator.evaluate("(1).__class__.__bases__")
        assert result["success"] is False

    # Edge cases
    def test_negative_numbers(self):
        """Test negative numbers."""
        result = self.evaluator.evaluate("-5+3")
        assert result["success"] is True
        assert result["result"] == Decimal("-2")

    def test_large_numbers(self):
        """Test large numbers."""
        result = self.evaluator.evaluate("999999*999999")
        assert result["success"] is True
        assert result["result"] == Decimal("999998000001")

    def test_complex_expression(self):
        """Test complex multi-operator expression."""
        result = self.evaluator.evaluate("(2+3)*4-8/2+1")
        assert result["success"] is True
        assert result["result"] == Decimal("17")

    # Result type verification
    def test_result_is_decimal_type(self):
        """Test that result is Decimal type."""
        result = self.evaluator.evaluate("5+3")
        assert result["success"] is True
        assert isinstance(result["result"], Decimal)

    def test_result_not_float(self):
        """Test that result is NOT float type."""
        result = self.evaluator.evaluate("0.1+0.2")
        assert result["success"] is True
        assert not isinstance(result["result"], float)
