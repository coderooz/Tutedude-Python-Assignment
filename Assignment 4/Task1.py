#Assignment 4/Task1.py


try:
    file = open('sample.txt', 'r')
    i = 1
    for l in file.readlines():
        print(f'Line {i}: {l}')
        i+=1
    file.close()
except:
    print('Error: File not found or error in opening the file.')
