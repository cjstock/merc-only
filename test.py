import numpy as np

matrix = [[1,2,3],[4,5,6],[7,8,9]]

output = []

state = 'right'

while matrix:
    if state == 'right':
        output.append(*(matrix.pop(0)))

print(output)