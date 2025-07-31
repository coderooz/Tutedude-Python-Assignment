# Assignment 3/Task2.py

import math

def math_operations(num: float) -> None:
    '''
    math_operations
    ----------------
    Performs the following operations using math module:
    - Square root
    - Natural logarithm (base e)
    - Sine (in radians)

    :param num: float, the number on which to perform operations
    '''
    if num < 0:
        print("Square root and logarithm cannot be calculated for negative numbers.")
        return

    print(f"Given number: {num}")
    print(f"Square root: {math.sqrt(num)}")
    print(f"Natural log (ln): {math.log(num)}")
    print(f"Sine (in radians): {math.sin(num)}")

try:
    value = float(input("Enter a number: "))
    math_operations(value)
except ValueError:
    print("Invalid input. Please enter a valid number.")
