"""
Tests for CalculatorEngine orchestrator.
Tests integration of validator + evaluator with Decimal precision and formatting.
"""
import pytest
from decimal import Decimal
from src.calculator.logic.calculator import CalculatorEngine


class TestCalculatorEngine:
    """Test suite for CalculatorEngine orchestrator."""

    def setup_method(self):
        """Initialize calculator before each test."""
        self.calc = CalculatorEngine()

    # Basic arithmetic integration tests
    def test_calculate_addition(self):
        """Test addition through full pipeline."""
        result = self.calc.calculate("2+3")
        assert result["success"] is True
        assert result["result"] == "5"

    def test_calculate_subtraction(self):
        """Test subtraction through full pipeline."""
        result = self.calc.calculate("10-4")
        assert result["success"] is True
        assert result["result"] == "6"

    def test_calculate_multiplication(self):
        """Test multiplication through full pipeline."""
        result = self.calc.calculate("3*7")
        assert result["success"] is True
        assert result["result"] == "21"

    def test_calculate_division(self):
        """Test division through full pipeline."""
        result = self.calc.calculate("8/2")
        assert result["success"] is True
        assert result["result"] == "4"

    # Decimal precision tests (critical!)
    def test_decimal_precision_exact(self):
        """Test that 0.1+0.2 returns exactly '0.3' as string."""
        result = self.calc.calculate("0.1+0.2")
        assert result["success"] is True
        assert result["result"] == "0.3"

    def test_decimal_precision_no_trailing_zeros(self):
        """Test that result has no unnecessary trailing zeros."""
        result = self.calc.calculate("1.0+2.0")
        assert result["success"] is True
        assert result["result"] == "3"  # Not "3.0" or "3.000"

    def test_decimal_precision_multiple_operations(self):
        """Test Decimal precision with multiple operations."""
        result = self.calc.calculate("0.1+0.1+0.1")
        assert result["success"] is True
        assert result["result"] == "0.3"

    # Parentheses integration tests
    def test_parentheses_simple(self):
        """Test simple parentheses: (2+3)*4=20."""
        result = self.calc.calculate("(2+3)*4")
        assert result["success"] is True
        assert result["result"] == "20"

    def test_parentheses_nested(self):
        """Test nested parentheses: ((1+2)*(3+4))=21."""
        result = self.calc.calculate("((1+2)*(3+4))")
        assert result["success"] is True
        assert result["result"] == "21"

    def test_parentheses_multiple_groups(self):
        """Test multiple parentheses groups."""
        result = self.calc.calculate("(2+3)*(4-1)")
        assert result["success"] is True
        assert result["result"] == "15"

    # Error handling tests
    def test_empty_expression_error(self):
        """Test empty expression shows Polish error."""
        result = self.calc.calculate("")
        assert result["success"] is False
        assert "puste" in result["error"].lower()

    def test_division_by_zero_error(self):
        """Test division by zero shows correct Polish error."""
        result = self.calc.calculate("5/0")
        assert result["success"] is False
        # Must match: "Nie mozna dzielic przez zero"
        error_lower = result["error"].lower()
        assert "nie" in error_lower and "zero" in error_lower

    def test_unbalanced_parentheses_error(self):
        """Test unbalanced parentheses shows error with position."""
        result = self.calc.calculate("(2+3")
        assert result["success"] is False
        assert "pozycji" in result["error"] or "brak" in result["error"].lower()

    def test_unbalanced_parentheses_extra_close(self):
        """Test extra closing parenthesis."""
        result = self.calc.calculate("2+3)")
        assert result["success"] is False

    # Validation catches errors before evaluation
    def test_validation_blocks_invalid_syntax(self):
        """Test that validator blocks invalid syntax before evaluation."""
        result = self.calc.calculate("2++3")
        assert result["success"] is False

    def test_validation_blocks_trailing_operator(self):
        """Test that validator blocks trailing operators."""
        result = self.calc.calculate("2+3+")
        assert result["success"] is False

    # Complex integration tests
    def test_complex_expression(self):
        """Test complex multi-operator expression."""
        result = self.calc.calculate("(2+3)*4-8/2+1")
        assert result["success"] is True
        assert result["result"] == "17"

    def test_unary_minus(self):
        """Test unary minus support."""
        result = self.calc.calculate("-5+3")
        assert result["success"] is True
        assert result["result"] == "-2"

    def test_unary_minus_in_parentheses(self):
        """Test unary minus inside parentheses."""
        result = self.calc.calculate("(-5)+3")
        assert result["success"] is True
        assert result["result"] == "-2"

    # Result formatting tests
    def test_result_is_string(self):
        """Test that result is returned as string."""
        result = self.calc.calculate("2+3")
        assert result["success"] is True
        assert isinstance(result["result"], str)

    def test_large_result_formatted(self):
        """Test large numbers are properly formatted."""
        result = self.calc.calculate("999999*2")
        assert result["success"] is True
        assert result["result"] == "1999998"

    def test_decimal_result_formatted(self):
        """Test decimal results are properly formatted."""
        result = self.calc.calculate("1/2")
        assert result["success"] is True
        assert result["result"] == "0.5"

    # Decimal context verification
    def test_high_precision_maintained(self):
        """Test that high precision calculations work."""
        result = self.calc.calculate("1/3*3")
        assert result["success"] is True
        # Should be "1" due to precision and rounding
        assert result["result"] == "1"
