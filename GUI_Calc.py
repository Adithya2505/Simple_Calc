"""
Calculator GUI Application
Implements the user interface using Tkinter
"""

import tkinter as tk
from operations import CalculatorOperations

class CalculatorApp:
    def __init__(self, root):
        """Initialize the calculator application"""
        self.root = root
        self.root.title("Calculator")
        
        # Window configuration
        self.root.resizable(False, False)  # Disable window resizing
        self.root.attributes('-toolwindow', True)  # Remove maximize button
        
        # Initialize calculator engine
        self.calculator = CalculatorOperations()
        
        # Setup UI components
        self.setup_display()
        self.setup_buttons()
    
    def setup_display(self):
        """Create the display area with clear button and result display"""
        display_frame = tk.Frame(self.root)
        display_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=5)
        
        # Clear button (positioned left of display)
        self.clear_btn = tk.Button(
            display_frame, 
            text="C", 
            width=5, 
            height=2,
            font=('Arial', 14), 
            command=self.on_clear_click
        )
        self.clear_btn.pack(side="left", padx=(0, 5))
        
        # Calculator display (read-only text field)
        self.display_var = tk.StringVar()
        self.display_var.set("0")  # Initialize with zero
        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=('Arial', 24),
            width=10,
            borderwidth=4,
            justify='right',
            readonlybackground='white',
            state='readonly'
        )
        self.display.pack(side="left", expand=True, fill="x")
    
    def setup_buttons(self):
        """Create calculator buttons in grid layout"""
        # Button layout specification:
        # (text, row, column) with operations ordered +, -, ×, ÷ bottom to top
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3),  # Top row
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('×', 2, 3),   # 2nd row
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),    # 3rd row
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3)     # Bottom row
        ]
        
        for (text, row, col) in buttons:
            # Create different button types based on their function
            if text in ['+', '-', '×', '÷']:
                btn = tk.Button(
                    self.root,
                    text=text,
                    width=5,
                    height=2,
                    font=('Arial', 14),
                    command=lambda t=text: self.on_operator_click(t)
                )
            elif text == '=':
                btn = tk.Button(
                    self.root,
                    text=text,
                    width=5,
                    height=2,
                    font=('Arial', 14),
                    command=self.on_equals_click
                )
            elif text == '.':
                btn = tk.Button(
                    self.root,
                    text=text,
                    width=5,
                    height=2,
                    font=('Arial', 14),
                    command=self.on_decimal_click
                )
            else:  # Number buttons
                btn = tk.Button(
                    self.root,
                    text=text,
                    width=5,
                    height=2,
                    font=('Arial', 14),
                    command=lambda t=text: self.on_digit_click(t)
                )
            
            # Position button in grid (row+1 to account for display row)
            btn.grid(row=row+1, column=col, padx=2, pady=2)
    
    # Event handlers with detailed docstrings
    def on_digit_click(self, digit):
        """Handle digit button presses (0-9)"""
        current = self.display_var.get()
        if current == '0' or self.calculator.reset_next_input:
            current = ''
            self.calculator.reset_next_input = False
            self.calculator.has_decimal = False
        self.display_var.set(current + digit)
    
    def on_decimal_click(self):
        """Handle decimal point button press"""
        current = self.display_var.get()
        if self.calculator.reset_next_input:
            current = '0'
            self.calculator.reset_next_input = False
            self.calculator.has_decimal = False
        
        # Only add decimal if none exists in current number
        if '.' not in current and not self.calculator.has_decimal:
            self.display_var.set(current + '.')
            self.calculator.has_decimal = True
    
    def on_operator_click(self, operator):
        """Handle operation button presses (+, -, ×, ÷)"""
        try:
            current_value = float(self.display_var.get())
        except ValueError:
            current_value = 0  # Default to 0 if display is invalid
            
        # Perform pending operation if one exists
        if self.calculator.operation and not self.calculator.reset_next_input:
            result = self.calculator.calculate(
                self.calculator.current_value, 
                current_value, 
                self.calculator.operation
            )
            self.display_var.set(str(result))
            self.calculator.current_value = result if result != "Error" else 0
        else:
            self.calculator.current_value = current_value
            
        # Store new operation and prepare for next input
        self.calculator.operation = operator
        self.calculator.reset_next_input = True
        self.calculator.has_decimal = False
    
    def on_equals_click(self):
        """Handle equals button press to complete calculation"""
        try:
            current_value = float(self.display_var.get())
        except ValueError:
            current_value = 0
            
        if self.calculator.operation:
            result = self.calculator.calculate(
                self.calculator.current_value, 
                current_value, 
                self.calculator.operation
            )
            self.display_var.set(str(result))
            self.calculator.current_value = result if result != "Error" else 0
            self.calculator.operation = None
            self.calculator.reset_next_input = True
            self.calculator.has_decimal = '.' in str(result)
    
    def on_clear_click(self):
        """Handle clear button press to reset calculator"""
        self.display_var.set(self.calculator.clear())

if __name__ == "__main__":
    # Create and run the application
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()