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


class TestScientificFunctions:
    """Test suite for scientific functions in SafeEvaluator."""

    def setup_method(self):
        """Initialize evaluator before each test."""
        self.evaluator = SafeEvaluator()

    # Trigonometric functions - degrees mode (default)
    def test_sin_90_degrees(self):
        """Test sin(90) = 1 in degrees mode."""
        result = self.evaluator.evaluate("sin(90)")
        assert result["success"] is True
        assert abs(result["result"] - Decimal("1.0")) < Decimal("0.0001")

    def test_cos_0_degrees(self):
        """Test cos(0) = 1 in degrees mode."""
        result = self.evaluator.evaluate("cos(0)")
        assert result["success"] is True
        assert abs(result["result"] - Decimal("1.0")) < Decimal("0.0001")

    def test_tan_45_degrees(self):
        """Test tan(45) = 1 in degrees mode."""
        result = self.evaluator.evaluate("tan(45)")
        assert result["success"] is True
        assert abs(result["result"] - Decimal("1.0")) < Decimal("0.0001")

    def test_sin_0_degrees(self):
        """Test sin(0) = 0 in degrees mode."""
        result = self.evaluator.evaluate("sin(0)")
        assert result["success"] is True
        assert abs(result["result"]) < Decimal("0.0001")

    def test_cos_90_degrees(self):
        """Test cos(90) = 0 in degrees mode."""
        result = self.evaluator.evaluate("cos(90)")
        assert result["success"] is True
        assert abs(result["result"]) < Decimal("0.0001")

    # Trigonometric functions - radians mode
    def test_sin_pi_over_2_radians(self):
        """Test sin(pi/2) = 1 in radians mode."""
        self.evaluator.set_angle_mode("radians")
        result = self.evaluator.evaluate("sin(pi/2)")
        assert result["success"] is True
        assert abs(result["result"] - Decimal("1.0")) < Decimal("0.0001")

    def test_cos_pi_radians(self):
        """Test cos(pi) = -1 in radians mode."""
        self.evaluator.set_angle_mode("radians")
        result = self.evaluator.evaluate("cos(pi)")
        assert result["success"] is True
        assert abs(result["result"] - Decimal("-1.0")) < Decimal("0.0001")

    def test_angle_mode_switch(self):
        """Test switching between angle modes."""
        # Default degrees: sin(90) = 1
        result1 = self.evaluator.evaluate("sin(90)")
        assert abs(result1["result"] - Decimal("1.0")) < Decimal("0.0001")

        # Switch to radians: sin(90) != 1 (sin(90 rad) is different)
        self.evaluator.set_angle_mode("radians")
        result2 = self.evaluator.evaluate("sin(90)")
        assert abs(result2["result"] - Decimal("1.0")) > Decimal("0.01")

        # Switch back to degrees: sin(90) = 1 again
        self.evaluator.set_angle_mode("degrees")
        result3 = self.evaluator.evaluate("sin(90)")
        assert abs(result3["result"] - Decimal("1.0")) < Decimal("0.0001")

    # Square root
    def test_sqrt_4(self):
        """Test sqrt(4) = 2."""
        result = self.evaluator.evaluate("sqrt(4)")
        assert result["success"] is True
        assert result["result"] == Decimal("2.0")

    def test_sqrt_9(self):
        """Test sqrt(9) = 3."""
        result = self.evaluator.evaluate("sqrt(9)")
        assert result["success"] is True
        assert result["result"] == Decimal("3.0")

    def test_sqrt_negative_error(self):
        """Test sqrt of negative number returns error."""
        result = self.evaluator.evaluate("sqrt(-1)")
        assert result["success"] is False
        assert "dziedziną" in result["error"].lower()

    # Logarithms
    def test_log_100(self):
        """Test log(100) = 2 (base-10)."""
        result = self.evaluator.evaluate("log(100)")
        assert result["success"] is True
        assert abs(result["result"] - Decimal("2.0")) < Decimal("0.0001")

    def test_log_1000(self):
        """Test log(1000) = 3 (base-10)."""
        result = self.evaluator.evaluate("log(1000)")
        assert result["success"] is True
        assert abs(result["result"] - Decimal("3.0")) < Decimal("0.0001")

    def test_ln_e(self):
        """Test ln(e) = 1 (natural log)."""
        result = self.evaluator.evaluate("ln(e)")
        assert result["success"] is True
        assert abs(result["result"] - Decimal("1.0")) < Decimal("0.0001")

    def test_log_negative_error(self):
        """Test log of negative number returns error."""
        result = self.evaluator.evaluate("log(-1)")
        assert result["success"] is False
        assert result["error"] is not None

    # Power operator (^)
    def test_power_2_3(self):
        """Test 2^3 = 8."""
        result = self.evaluator.evaluate("2^3")
        assert result["success"] is True
        assert result["result"] == Decimal("8")

    def test_power_2_10(self):
        """Test 2^10 = 1024."""
        result = self.evaluator.evaluate("2^10")
        assert result["success"] is True
        assert result["result"] == Decimal("1024")

    def test_power_3_2(self):
        """Test 3^2 = 9."""
        result = self.evaluator.evaluate("3^2")
        assert result["success"] is True
        assert result["result"] == Decimal("9")

    def test_power_with_parentheses(self):
        """Test (2+3)^2 = 25."""
        result = self.evaluator.evaluate("(2+3)^2")
        assert result["success"] is True
        assert result["result"] == Decimal("25")

    # Factorial
    def test_factorial_5(self):
        """Test factorial(5) = 120."""
        result = self.evaluator.evaluate("factorial(5)")
        assert result["success"] is True
        assert result["result"] == Decimal("120")

    def test_factorial_0(self):
        """Test factorial(0) = 1."""
        result = self.evaluator.evaluate("factorial(0)")
        assert result["success"] is True
        assert result["result"] == Decimal("1")

    def test_factorial_10(self):
        """Test factorial(10) = 3628800."""
        result = self.evaluator.evaluate("factorial(10)")
        assert result["success"] is True
        assert result["result"] == Decimal("3628800")

    def test_factorial_negative_error(self):
        """Test factorial(-1) returns Polish error message."""
        result = self.evaluator.evaluate("factorial(-1)")
        assert result["success"] is False
        assert "silnia" in result["error"].lower()
        assert "ujemnych" in result["error"].lower()

    def test_factorial_not_integer_error(self):
        """Test factorial(5.5) returns Polish error message."""
        result = self.evaluator.evaluate("factorial(5.5)")
        assert result["success"] is False
        assert "silnia" in result["error"].lower()
        assert "całkowitej" in result["error"].lower()

    def test_factorial_too_large_error(self):
        """Test factorial(171) returns Polish error message."""
        result = self.evaluator.evaluate("factorial(171)")
        assert result["success"] is False
        assert "silnia" in result["error"].lower()

    # Mathematical constants
    def test_pi_constant(self):
        """Test pi constant is available."""
        result = self.evaluator.evaluate("pi")
        assert result["success"] is True
        assert abs(result["result"] - Decimal("3.14159")) < Decimal("0.001")

    def test_e_constant(self):
        """Test e constant is available."""
        result = self.evaluator.evaluate("e")
        assert result["success"] is True
        assert abs(result["result"] - Decimal("2.71828")) < Decimal("0.001")

    def test_pi_in_expression(self):
        """Test pi constant in expression: 2*pi."""
        result = self.evaluator.evaluate("2*pi")
        assert result["success"] is True
        assert abs(result["result"] - Decimal("6.28318")) < Decimal("0.001")

    # Complex expressions
    def test_complex_expression_with_functions(self):
        """Test complex expression: sin(45) + sqrt(4)."""
        result = self.evaluator.evaluate("sin(45) + sqrt(4)")
        assert result["success"] is True
        # sin(45 deg) ≈ 0.707, sqrt(4) = 2, total ≈ 2.707
        assert abs(result["result"] - Decimal("2.707")) < Decimal("0.01")

    def test_complex_expression_with_power(self):
        """Test complex expression: 2^3 + 3^2."""
        result = self.evaluator.evaluate("2^3 + 3^2")
        assert result["success"] is True
        assert result["result"] == Decimal("17")

    def test_nested_functions(self):
        """Test nested functions: sqrt(log(100))."""
        result = self.evaluator.evaluate("sqrt(log(100))")
        assert result["success"] is True
        # log(100) = 2, sqrt(2) ≈ 1.414
        assert abs(result["result"] - Decimal("1.414")) < Decimal("0.01")
