# Assignment 2/Task1.py

def checkNum(num: int) -> None:
    '''
    checkNum
    ---------
    Check if the given number is even or odd.

    :params
    - num (int): Takes the number input from user.

    :returns
    - None
    '''
    r = f'The given number({num}) is'
    if num % 2 == 0:
        print(f'{r} even.')
    else:
        print(f'{r} odd.')

de = int(input('Enter any number: '))
checkNum(de)
