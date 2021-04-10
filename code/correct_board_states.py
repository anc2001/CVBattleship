import numpy as np

# 0 -> nothing, 1 -> miss, 2 -> hit
template = np.zeros((10,10))

def converter(moves, board):
    for string in moves:
        if len(string) == 3:
            row = ord(string[0])-65
            if not (row >= 0 and row <= 9):
                raise Exception('First digit out of range')
            column = int(string[1]) - 1
            if not (column >= 0 and column <= 9):
                raise Exception('Second digit is out of range')
            value = 0
            if ord(string[2]) == 72:
                value = 2
            elif ord(string[2]) == 77:
                value = 1
            else:
                raise Exception('last digit must be H or M')
            board[row][column] = value
        else:
            raise Exception('Strings must be of format <char><int>')

    return board

# Background
background = np.zeros((4,10,10))
background[0] = template
background[1] = converter(["H3M", "F6M"], template)
background[2] = converter(["B3M", "B4H", "B5H", "B6M", "D8M", "E2M", "E9M", "F2H", "F6M", "G8M", "H3M", "H7M", "H8M", "I4M"], template)
print(background[2])
