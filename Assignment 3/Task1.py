# Assignment 3/Task1.py

def factorial(num : int) -> int :
    if num < 2:
        return 1
    else:
        return num * factorial(num-1)

inNum = int(input('Input a number: '))

print('Result of the inserted number is: ', factorial(inNum))