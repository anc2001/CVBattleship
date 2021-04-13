import numpy as np

#Functionally abstract class, should never be instantiated
class PlayerInterface: 
    # Constructor for player class, 
    # opp_board 10 x 10 board representing the top board, should only range from 0-2.
    # 0 -> nothing, 1 -> miss, 2 -> hit
    # own_board 10 x 10 board representing the bottom board, should only range from 0-4
    # values explained in binary 
    # 00 -> no ship, nothing
    # 01 -> no ship, miss
    # 10 -> ship, nothing
    # 11 -> ship, hit
    # battleship 5 x 4 array, each array is a battleship, the 4x1 internal array is of the
    # form [row_or_col, shared_val, start, end]
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
    # board and returns 1 the move is valid and makes change, returns 0
    # if the move is invalid
    def receive_turn(self, move):
        pass

    #Takes in 10 x 10 and suggests a move if AI, just polls if human
    def suggest_turn(self, array):
        pass

    #Takes in move of specificed format, this guaranteed to be a valid move, 
    # so just edit the opposing board
    def make_turn(self, move):
        if len(move == 3):
            row = ord(move[0])-65
            column = int(move[1]) - 1
            if ord(move[2]) == 72:
                value = 2
            elif ord(move[2]) == 77:
                value = 1
            self.opp_board[row][column] = value
        else:
            row = ord(move[0])-65
            column = int(move[1:3]) - 1
            if ord(move[3]) == 72:
                value = 2
            elif ord(move[3]) == 77:
                value = 1
            self.opp_board[row][column] = value  
        return 0
    