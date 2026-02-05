"""
SciCalc - Main Entry Point
"""

from src.calculator.controller.calculator_controller import CalculatorController


def main():
    """
    Main application entry point - launches GUI calculator.
    """
    controller = CalculatorController()
    controller.run()


if __name__ == "__main__":
    main()
