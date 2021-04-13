import numpy as np

#Functionally abstract class, should never be instantiated
class PlayerInterface: 
    # Constructor for player class, 
    # opp_board 10 x 10 board representing the top board, should only range from 0-2.
    # 0 -> nothing, 1 -> miss, 2 -> hit
    # own_board 10 x 10 board representing the bottom board, should only range from 0-3
    # values explained in binary 
    # 00 -> no ship, nothing
    # 01 -> no ship, miss
    # 10 -> ship, nothing
    # 11 -> ship, hit
    # battleship 5 x 4 array, each array is a battleship, the 4x1 internal array is of the
    # form ['row', 'col', 'orientation', 'ship size']
    # battleship_sunk 5 x 1 array, each array is a boolean value of 
    def __init__(self):
        self.opp_board = np.zeros((10,10))
        self.own_board = np.zeros((10,10))
        self.battleships = np.zeros((5,4))
        self.battleship_sunk = np.zeros((5,))
    
    # Returns true if this player has lost, false otherwise
    def has_not_lost(self):
        return_val = 1
        for i in self.battleship_sunk:
            return_val = return_val and i
        return return_val
    
    # Prints top board, probably change this to make it nicer
    def show_opp_board(self):
        print(self.opp_board)
    
    # Prints bottom board, probably change this to make it nicer 
    def show_own_board(self):
        print(self.own_board)

    # Receives move of specified format letter followed by integer, changes
    # board and returns 1 if the move is valid and makes change, returns 0
    # if the move is invalid
    def receive_turn(self, move):
        def convert_command(move):
            row = 0
            column = 0
            if len(move) == 2:
                row = ord(move[0])-65
                if not (row >= 0 and row <= 9):
                    return 0
                column = int(move[1]) - 1
                if not (column >= 0 and column <= 9):
                    return 0
                else:
                    return 0
            elif len(move) == 3:
                row = ord(move[0])-65
                if not (row >= 0 and row <= 9):
                    return 0
                column = int(move[1:3]) - 1
                if not column == 9:
                    return 0
            else:
                return 0
        return (row, column)



        coord = self.convert_command(move)
        if not coord:
            return 0
        
        row = coord[0]
        column = coord[1]
        if 1 and self.own_board[row][column]:
            print("Already tried to move there!")
            return 0

        if 2 and self.own_board[row][column]:
            self.own_board[row][column] = 3
            print("Hit!")
            self.check_if_sunk(coord)
        else:
            self.own_board[row][column] = 1
            print("Miss!")
        return 1

    #Called when coordinate value has hit a ship, checks if the associated ship
    #has been sunk, and sets value accordingly 
    def check_if_sunk(self, coord):
        for i in range(5):
            battleship = self.battleships[i]
            if int(battleship[0]) == coord[0] or int(battleship[1]) == coord[1]:
                for j in range()

        return

