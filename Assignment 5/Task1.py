#Assignment 5/Task1.py

data = {
    "Alice": 55,
    "Mark" : 87,
    "Ankur" : 77,
    "Sam" : 29
}

def checkMarks(name:str) -> None:
    '''
    checkMarks
    ----------
    This is a method that fetches the marks data from the file and prints out the marks of the give person.

    :param
    - name (str): The users name.
    '''
    global data
    if name in data:
        print(f'{name} got {data[name]} marks in exam.')
    else:
        print(f'Student({name}) not found.')


student = str(input('Enter the students name: '))
checkMarks(student)
