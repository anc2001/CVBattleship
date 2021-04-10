# A board is a list of rows, which will be filled in 1s and 0s
board = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
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
    print("  A B C D E F G H I J")
    print(" +-+-+-+-+-++-+-+-+-+-+")
    row_number = 1
    for row in board:
        print("%d|%s|" % (row_number, "|".join(row)))
        print(" +-+-+-+-+-++-+-+-+-+-+")
        row_number = row_number + 1


# 10 battleships - asks for 10 placements
for n in range(10):
    print("Where do you want ship ", n + 1, "?")
    row_number, column_number = ask_user_for_board_position()

    # repetition check
    if board[row_number][column_number] == '1':
        print("That spot already has a battleship in it!")

    board[row_number][column_number] = '1'
    print_board(board)


# Now clear the screen, and the other player starts guessing
print("\n"*50)

guesses_board = [
    [' ', ' ', ' ', ' ', ' ',' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
]


# Keep playing until we have 10 right guesses
guesses = 0
while guesses < 10:
    print("Guess a battleship location")
    row_number, column_number = ask_user_for_board_position()

    if guesses_board[row_number][column_number] != ' ':
        print("You have already guessed that place!")
        continue

    # repition check
    if board[row_number][column_number] == '1':
        print("HIT!")
        guesses_board[row_number][column_number] = '1'
        guesses = guesses + 1
    else:
        guesses_board[row_number][column_number] = '0'
        print("MISS!")

    print_board(guesses_board)
print("GAME OVER!")

