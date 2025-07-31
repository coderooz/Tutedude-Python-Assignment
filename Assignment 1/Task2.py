

def greatingCode(first: str, last: str): 
    return f'Greetings! {first} {last}.'


first = str(input('Enter your first name: '))
last = str(input('Enter your last name: '))

print(greatingCode(first, last))