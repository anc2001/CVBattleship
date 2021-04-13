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
        self.battleships = []
        self.battleship_coords = []
        self.battleship_sunk = np.zeros((5,))
    
    # Returns true if this player has lost, false otherwise
    def has_lost(self):
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

    def set_own_board(self):
        def info_to_coordinates(row, col, orientation, size):
            coordinates = []
            if orientation == 'up':
                for i in range(size):
                    coordinates.append(chr(ord(row) - i) + col)
            elif orientation == 'down':
                for i in range(size):
                    coordinates.append(chr(ord(row) + i) + col)
            elif orientation == 'left':
                for i in range(size):
                    coordinates.append(row + str((int(col) - i)))
            elif orientation == 'right':
                for i in range(size):
                    coordinates.append(row + str((int(col) + i)))
            return coordinates

        def converter(moves):
            coordinates = []
            for move in moves:
                if len(move) == 2:
                    row = ord(move[0])-65
                    column = int(move[1]) - 1
                    self.own_board[row][column] = 2
                elif len(move) == 3:
                    row = ord(move[0])-65
                    column = int(move[1:3]) - 1
                    self.own_board[row][column] = 2
                coordinates.append((row, column))
            return coordinates  

        for i in range(5):
            ship = self.battleships[i]
            coords = info_to_coordinates(ship[0], ship[1], ship[2], ship[3])
            self.battleship_coords.append(converter(coords))

    # Receives move of specified format letter followed by integer, changes
    # board and returns 1 if the move is valid and misses, returns 2 if the 
    # move is valid and hits, returns 0 if the move is invalid
    def receive_turn(self, move):

        def check_if_sunk(row, col):
            for i in range(5):
                ship_coordinates = self.battleship_coords[i]
                for coord in ship_coordinates:
                    if coord == (row, col):
                        flag = 4
                        for (x,y) in ship_coordinates:
                            flag = flag & int(self.own_board[x][y])
                        if flag == 4:
                            self.battleship_sunk[i] = 1
                            return 1
                        return 0
            return 0
        
        row = 0
        column = 0
        if len(move) == 2:
            row = ord(move[0])-65
            if not (row >= 0 and row <= 9):
                return 0
            column = int(move[1]) - 1
            if not (column >= 0 and column <= 9):
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
        
        if 1 & int(self.own_board[row][column]):
            print("Already tried to move there!")
            return 0

        if 2 & int(self.own_board[row][column]):
            self.own_board[row][column] = 3
            print("Hit!")
            sunk = check_if_sunk(row, column)
            if sunk: 
                print("You sunk one as well!")
                return 3
            else:
                return 2
        else:
            self.own_board[row][column] = 1
            print("Miss!")
            return 1
