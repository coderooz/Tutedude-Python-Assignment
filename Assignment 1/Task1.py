
def addNum(a, b):
    return a + b 

def subNum(a, b):
    return a - b

def mulNum(a, b):
    return a * b

def divNum(a, b):
    return a / b

Num1 = float(input('Enter any number 1: '))
Num2 = float(input('Enter any number 2: '))


print('Addition: ' + str(addNum(Num1, Num2)))
print('Subtraction: '  + str(subNum(Num1, Num2)))
print('Multiplication: ' + str(mulNum(Num1, Num2)))
print('Divition: '  + str(divNum(Num1, Num2)))

