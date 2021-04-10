# A board is a list of rows, which will be filled in 1s and 0s
board = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]

# letter to number
letters_to_numbers = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'I': 8,
    'J': 9
}

def converter(moves, board):
    for string in moves:
        if len(string) == 3:
            row = ord(string[0])-65
            if not (row >= 0 and row <= 9):
                raise Exception('First digit out of range')
            column = int(string[1]) - 1
            if string not in "ABCDEFGHIJ" :
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

def parser():   
    col = input("Enter a column letter and row number")
    if not(len(col) == 2) :
        return ""
    if(col[0] not in "ABCDEFGHIJ"):
        return ""
    if(ord(col[1])-65 <0 or ord(col[1])-65 > 9 ) :
        return ""
    else :
        return col




# check if valid position
def ask_user_for_board_position():
    column = input("column (A to J):")
    while column not in "ABCDEFGHIJ":
        print("Wrong column number")
        column = input("column (A to J):")
    

    row = input("row (1 to 10):")
    while row not in "12345678910":
        print("Wrong row number")
        row = input("row (1 to 10):")

    return int(row) - 1, letters_to_numbers[column]


def print_board(board):
    # Show the board, one row at a time
    print(board[2])


# 10 battleships - asks for 10 placements
board = [
    [2,0,0,0,0,0,0,0,0,0],
    [2,0,0,0,0,0,0,0,2,0],
    [2,0,0,0,0,0,0,0,2,0],
    [2,0,0,0,0,0,0,0,2,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,2,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]


# Now clear the screen, and the other player starts guessing


guesses_board = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]


# Keep playing until we have 10 right guesses
guesses = 0
while guesses < 10:
    print("Guess a battleship location")
    n = parser()
    if not(n == ""):
        row = int(n[1])
        col = letters_to_numbers[n[0]]
        if(board[row][col] == 2):
            b = converter([n + "H"], guesses_board)
        else :
            b = converter([n + "M"], guesses_board)
    
        guesses_board = b
        print_board(guesses_board)
print("GAME OVER!")
