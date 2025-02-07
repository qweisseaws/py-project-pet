import tkinter as tk
from math import isclose


class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Калькулятор")
        self.master.geometry("400x600")

        self.main_label = tk.Label(master, text="0", font=("Arial", 24), anchor="e", padx=10)
        self.main_label.pack(side="bottom", fill="both", expand=True)

        self.secondary_label = tk.Label(master, text="", font=("Arial", 14), anchor="e", padx=10)
        self.secondary_label.pack(side="bottom", fill="both", expand=True)

        self.create_buttons()
        self.clear()

    def create_buttons(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack(side="top", fill="both", expand=True)

        button_grid = [
            ("7", 1, 1), ("8", 1, 2), ("9", 1, 3), ("/", 1, 4),
            ("4", 2, 1), ("5", 2, 2), ("6", 2, 3), ("*", 2, 4),
            ("1", 3, 1), ("2", 3, 2), ("3", 3, 3), ("-", 3, 4),
            ("0", 4, 1), (".", 4, 2), ("+/-", 4, 3), ("+", 4, 4),
            ("C", 5, 1), ("CE", 5, 2), ("=", 5, 3), ("00", 5, 4),
        ]

        self.buttons = {}

        for text, row, col in button_grid:
            button = tk.Button(button_frame, text=text, font=("Arial", 18),
                               command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky="nsew")
            self.buttons[text] = button

        # Configure row and column weights
        for i in range(1, 6):
            button_frame.grid_rowconfigure(i, weight=1)
            button_frame.grid_columnconfigure(i, weight=1)

    def clear(self):
        self.first_operand = None
        self.operator = None
        self.clear_entry()

    def clear_entry(self):
        self.current_input = "0"
        self.update_display()

    def on_button_click(self, button_text):
        if button_text.isdigit() or button_text == ".":
            self.handle_digit(button_text)
        elif button_text in ["+", "-", "*", "/"]:
            self.handle_operator(button_text)
        elif button_text == "=":
            self.calculate_result()
        elif button_text == "C":
            self.clear()
        elif button_text == "CE":
            self.clear_entry()
        elif button_text == "+/-":
            self.toggle_sign()

    def handle_digit(self, digit):
        if digit == "." and "." in self.current_input:
            return  # Ignore additional dots in the number

        if self.current_input == "0" or self.current_input == "-0":
            self.current_input = digit
        else:
            self.current_input += digit

        self.update_display()

    def handle_operator(self, operator):
        if self.operator:
            self.calculate_result()

        self.first_operand = float(self.current_input)
        self.operator = operator
        self.clear_entry()
        self.update_secondary_display()

    def calculate_result(self):
        if self.operator and self.current_input:
            second_operand = float(self.current_input)
            try:
                if self.operator == "+":
                    result = self.first_operand + second_operand
                elif self.operator == "-":
                    result = self.first_operand - second_operand
                elif self.operator == "*":
                    result = self.first_operand * second_operand
                elif self.operator == "/":
                    result = self.first_operand / second_operand
            except ZeroDivisionError:
                self.show_error("ОШИБКА")
                return

            if isclose(result, int(result)):
                result = int(result)

            self.first_operand = result
            self.clear_entry()
            self.update_secondary_display()
            self.update_display()

            # Reset operator after calculation
            self.operator = None

    def toggle_sign(self):
        if self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input

            self.update_display()

    def update_display(self):
        self.main_label.config(text=self.format_number(self.current_input))

    def update_secondary_display(self):
        if self.operator:
            self.secondary_label.config(text=f"{self.format_number(self.first_operand)} {self.operator}")

    def format_number(self, number):
        if "." in str(number):
            return format(float(number), ".10f").rstrip("0").rstrip(".")
        else:
            return str(number)

    def show_error(self, message):
        self.main_label.config(text=message)
        self.secondary_label.config(text="")
        self.first_operand = None
        self.operator = None


if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()