# Assignment 6/Task1.py

import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Calculator")
        self.expression = ""

        # Entry field to display current expression/result
        self.input_text = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.input_text, font=('Arial', 18), bd=10, insertwidth=2, width=15,
                              borderwidth=4, relief='ridge', justify='right')
        self.entry.grid(row=0, column=0, columnspan=4)

        # Buttons layout
        buttons = [
            ('7', 1, 0),  ('8', 1, 1),  ('9', 1, 2),  ('/', 1, 3),
            ('4', 2, 0),  ('5', 2, 1),  ('6', 2, 2),  ('*', 2, 3),
            ('1', 3, 0),  ('2', 3, 1),  ('3', 3, 2),  ('-', 3, 3),
            ('0', 4, 0),  ('.', 4, 1),  ('=', 4, 2),  ('+', 4, 3),
            ('C', 5, 0),  ('←', 5, 1)
        ]

        for (text, row, col) in buttons:
            button = tk.Button(root, text=text, padx=20, pady=20, font=('Arial', 14),
                               command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky="nsew")

        # Make the grid expand when window resizes
        for i in range(6):
            self.root.rowconfigure(i, weight=1)
        for i in range(4):
            self.root.columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
        elif char == "←":
            self.expression = self.expression[:-1]
        elif char == "=":
            try:
                result = str(eval(self.expression))
                self.expression = result
            except Exception:
                self.expression = "Error"
        else:
            self.expression += str(char)

        self.input_text.set(self.expression)


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
