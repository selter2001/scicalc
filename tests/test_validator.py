"""
Tests for InputValidator module.
Tests parentheses validation, syntax checking, and Polish error messages.
"""
import pytest
from src.calculator.logic.validator import InputValidator


class TestInputValidator:
    """Test suite for InputValidator class."""

    def setup_method(self):
        """Initialize validator before each test."""
        self.validator = InputValidator()

    # Parentheses validation tests
    def test_balanced_parentheses_simple(self):
        """Test simple balanced parentheses."""
        result = self.validator.validate("(2+3)")
        assert result["valid"] is True
        assert result["error"] is None

    def test_balanced_parentheses_nested(self):
        """Test nested balanced parentheses."""
        result = self.validator.validate("((1+2)*(3+4))")
        assert result["valid"] is True
        assert result["error"] is None

    def test_balanced_parentheses_multiple(self):
        """Test multiple balanced parentheses groups."""
        result = self.validator.validate("(2+3)*(4+5)")
        assert result["valid"] is True
        assert result["error"] is None

    def test_unbalanced_parentheses_missing_close(self):
        """Test missing closing parenthesis with position info."""
        result = self.validator.validate("(2+3")
        assert result["valid"] is False
        assert "pozycji" in result["error"] or "brak" in result["error"].lower()
        assert result["position"] is not None

    def test_unbalanced_parentheses_missing_open(self):
        """Test missing opening parenthesis with position info."""
        result = self.validator.validate("2+3)")
        assert result["valid"] is False
        assert "pozycji" in result["error"] or "brak" in result["error"].lower()
        assert result["position"] is not None

    def test_unbalanced_parentheses_nested(self):
        """Test unbalanced nested parentheses."""
        result = self.validator.validate("((2+3)")
        assert result["valid"] is False
        assert result["position"] is not None

    # Empty expression tests
    def test_empty_expression(self):
        """Test empty expression shows Polish error."""
        result = self.validator.validate("")
        assert result["valid"] is False
        assert "puste" in result["error"].lower()

    def test_whitespace_only_expression(self):
        """Test whitespace-only expression treated as empty."""
        result = self.validator.validate("   ")
        assert result["valid"] is False
        assert "puste" in result["error"].lower()

    # Syntax validation tests
    def test_valid_basic_arithmetic(self):
        """Test valid basic arithmetic expressions."""
        expressions = ["2+3", "10-4", "3*7", "8/2"]
        for expr in expressions:
            result = self.validator.validate(expr)
            assert result["valid"] is True, f"Failed for: {expr}"

    def test_valid_complex_expression(self):
        """Test valid complex expression."""
        result = self.validator.validate("(2+3)*4-5/2")
        assert result["valid"] is True

    def test_unary_minus_allowed(self):
        """Test unary minus is allowed."""
        result = self.validator.validate("-5+3")
        assert result["valid"] is True

    def test_unary_minus_in_parentheses(self):
        """Test unary minus inside parentheses."""
        result = self.validator.validate("(-5)+3")
        assert result["valid"] is True

    def test_invalid_consecutive_operators(self):
        """Test consecutive operators are invalid."""
        result = self.validator.validate("2++3")
        assert result["valid"] is False

    def test_invalid_operator_at_end(self):
        """Test operator at end is invalid."""
        result = self.validator.validate("2+3+")
        assert result["valid"] is False

    def test_valid_decimal_numbers(self):
        """Test decimal numbers are valid."""
        result = self.validator.validate("0.1+0.2")
        assert result["valid"] is True

    def test_valid_large_numbers(self):
        """Test large numbers are valid."""
        result = self.validator.validate("999999+1")
        assert result["valid"] is True
