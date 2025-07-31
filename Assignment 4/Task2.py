#Assignment 4/Task2.py

fileName= 'output.txt'

# write data into a file.
winp = str(input('Enter Few words for the file: '))
file = open(fileName, 'w')
file.write(winp)
file.close()

# Append data into the file
aInp = str(input('Enter some more words into the file: '))
file = open(fileName, 'a')
file.write(aInp)
file.close()


with open(fileName, 'r') as file:
    print(f'File({fileName}) content: ',file.read())