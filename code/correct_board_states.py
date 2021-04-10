import numpy as np

# 0 -> nothing, 1 -> miss, 2 -> hit
def converter(moves, board):
    for string in moves:
        row = 0
        column = 0
        value = 0
        if len(string) == 3:
            row = ord(string[0])-65
            if not (row >= 0 and row <= 9):
                raise Exception('First digit out of range')
            column = int(string[1]) - 1
            if not (column >= 0 and column <= 9):
                raise Exception('Second digit is out of range')
            if ord(string[2]) == 72:
                value = 2
            elif ord(string[2]) == 77:
                value = 1
            else:
                raise Exception('last digit must be H or M')
        elif len(string) == 4:
            row = ord(string[0])-65
            if not (row >= 0 and row <= 9):
                raise Exception('First digit out of range')
            column = int(string[1:3]) - 1
            if not column == 9:
                raise Exception('Second digit is out of range')
            if ord(string[3]) == 72:
                value = 2
            elif ord(string[3]) == 77:
                value = 1
        else:
            raise Exception('Strings must be of format <char><int>')
        board[row][column] = value

    return board

# Background
background = np.zeros((4,10,10))
background[0] = converter([], np.zeros((10,10)))
converter(["H3M", "F6M"], background[1])
two = ["B3M", "B4H", "B5H", "B6M", "D8M", "E2M", "E9M", "F2H", "G8M", "H7M", "H8M", "I4M","H3M", "F6M"]
converter(two, background[2])
three = ["A6M", "C1M", "C8M", "D8M", "E5M", "E6M", "E9M", "F7H", "F8H", "F9H", "G2H", "H2H", "H4M", "H6M", "I2H", "J2H", "I10M"]
big = np.append(three, two)
converter(big, background[3])

#No Background
no_background = np.zeros((6,10,10))
first = ["C9M"]
converter(first, no_background[1])
second = np.append(["D5M", "H3M", "G7M"], first)
converter(second, no_background[2])
third = ["C3H", "C4H"]
third = np.append(third, second)
converter(third, no_background[3])
fourth = ["A3M", "B6M", "C2H", "E7M", "F2M", "F5M", "F8H", "F9H", "G4M", "I9M", "J7M"]
fourth = np.append(fourth, third)
converter(fourth, no_background[4])
fifth = ["A1M", "A5H", "A8M", "B3M", "B5H", "B10M", "C2M", "C3M", "C5H", "C6M", "C9M","C10M", "D1H", "D2H", "D3H", "D4H", "D5H", "D6M", "D9M"]
more = ["E4M", "E5H", "E6H", "E10H", "F1M", "F8M", "F10H", "G4M", "G6M", "G7M", "G10H", "H2M", "H3M", "H5H", "H6H", "H7H", "H8M", "H10H", "I3M", "I9M", "J3M", "J5M"]
fifth = np.append(fifth, more)
converter(fifth, no_background[5])