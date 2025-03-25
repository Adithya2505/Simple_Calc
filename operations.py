"""
Calculator Operations Module
Handles all mathematical operations and state management for the calculator
"""

class CalculatorOperations:
    def __init__(self):
        """Initialize calculator with default state"""
        self.current_value = 0      # Stores the first operand in calculations
        self.operation = None       # Stores the current operation (+, -, ×, ÷)
        self.reset_next_input = False  # Flag to clear display before next input
        self.has_decimal = False    # Tracks if current number has a decimal point

    def calculate(self, a, b, operation):
        """
        Perform arithmetic operation on two numbers
        Args:
            a: First operand
            b: Second operand
            operation: The arithmetic operation to perform
        Returns:
            Result of the operation or "Error" for division by zero
        """
        if operation == '+':
            return a + b
        elif operation == '-':
            return a - b
        elif operation == '×':
            return a * b
        elif operation == '÷':
            return a / b if b != 0 else "Error"  # Handle division by zero
        return b  # Return second operand if no operation specified

    def clear(self):
        """
        Reset calculator to initial state
        Returns:
            "0" as the default display value
        """
        self.current_value = 0
        self.operation = None
        self.reset_next_input = False
        self.has_decimal = False
        return "0"