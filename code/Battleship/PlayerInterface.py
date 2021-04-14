import numpy as np
from colorama import init 
from termcolor import colored 
import copy

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
        self.use_camera = 0
    
    # Returns true if this player has lost, false otherwise
    def has_lost(self):
        return_val = 1
        for i in self.battleship_sunk:
            return_val = return_val and i
        return return_val
    
    # Prints top board, probably change this to make it nicer
    def show_opp_board(self):
        board = copy.deepcopy(self.opp_board)
        board = np.where(board == 0, colored("O", 'grey' ,'on_blue'), 
        np.where(board == 1, colored("X", 'grey' ,'on_blue'), colored("X", 'grey' ,'on_red')))
        s = ""
        alph = 65
        print("  12345678910")
        for i in range(board.shape[0]) :
            for j in range(board.shape[1]): 
                s = s + board[i,j]
            print(chr(alph) + " " + s)
            alph+=1
            s = ""
    
    # Prints bottom board, probably change this to make it nicer 
    def show_own_board(self):
        board = copy.deepcopy(self.own_board)
        board = np.where(board == 0, colored("O", 'grey' ,'on_blue'), 
        np.where(board == 1, colored("X", 'grey' ,'on_blue'), 
        np.where(board == 2, colored("O", 'grey' ,'on_white'), colored("X", 'grey' ,'on_red'))))
        s = ""
        alph = 65
        print("  12345678910")
        for i in range(board.shape[0]) :
            for j in range(board.shape[1]): 
                s = s + board[i,j]
            print(chr(alph) + " " + s)
            alph+=1
            s = ""

    # Given coordinates, orientation, and size, return coordinates that battleship occupies
    def info_to_coordinates(self, row, col, orientation, size):
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

    #To do fill this in
    def place_battleships_camera(self):
        return []
    
    def set_own_board(self):
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
            coords = self.info_to_coordinates(ship[0], ship[1], ship[2], ship[3])
            self.battleship_coords.append(converter(coords))

    # Returns whether or not there is a conflict when adding a battleship to a coordinate
    def conflict_exists(self, battleship_info, row, col, orientation, size):
        if ((orientation == 'up' and ord(row) - 64 - size < 0) or 
            (orientation == 'down' and ord(row) - 64 + size > 11) or 
            (orientation == 'left' and int(col) - size < 0) or 
            (orientation == 'right' and int(col) + size > 11)):
            return True

        for (ship_row, ship_col, ship_orientation, ship_size) in battleship_info:
            ship_coordinates = self.info_to_coordinates(ship_row, ship_col, ship_orientation, ship_size)
            curr_coordinates = self.info_to_coordinates(row, col, orientation, size)

            if not set(ship_coordinates).isdisjoint(curr_coordinates):
                return True
        return False

    # Receives move of specified format letter followed by integer, changes
    # board and returns 1 if the move is valid and misses, returns 2 if the 
    # move is valid and hits, returns 0 if the move is invalid
    def receive_turn(self, move):

        def check_if_sunk(hit_row, hit_col):
            for i in range(5):
                ship_coordinates = self.battleship_coords[i]
                if not self.battleship_sunk[i]:
                    for coord in ship_coordinates:
                        if coord[0] == hit_row and coord[1] == hit_col: 
                            flag = 3
                            for (x,y) in ship_coordinates:
                                flag = flag & int(self.own_board[x][y])
                            if flag == 3:
                                self.battleship_sunk[i] = 1
                                return 1
                            return 0
            return 0

        def poll_for_change(h_or_m):
            #Just needs to check if the current board equals the one detected
            print("The other player wants to move at {}, place to continue the game!".format(move))
            return
        
        row = 0
        column = 0
        if len(move) == 2:
            row = ord(move[0])-65
            column = int(move[1]) - 1
        elif len(move) == 3:
            row = ord(move[0])-65
            column = int(move[1:3]) - 1
        
        if 1 & int(self.own_board[row][column]):
            print("Already tried to move there!")
            return 0

        if 2 & int(self.own_board[row][column]):
            self.own_board[row][column] = 3
            print("Hit!")
            sunk = check_if_sunk(row, column)
            #Note, this only returns 3 for when we go to train the neural network lol
            if sunk: 
                print("You sunk one as well!")
                if self.use_camera:
                    poll_for_change("H")
                return 3
            else:
                if self.use_camera:
                    poll_for_change("H")
                return 2
        else:
            self.own_board[row][column] = 1
            print("Miss!")
            if self.use_camera:
                poll_for_change("M")
            return 1
    
    # Takes in move of specificed format, this is guaranteed to be a valid move, 
    # so just edit the opposing board
    def make_turn(self, move):
        if len(move) == 3:
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
        
        if self.use_camera:
            #Poll for confirmational change, wait until the board matches our board
            print("Your move is valid, and the other player has confirmed it. Place your piece to continue!")
            return 0
        else:
            return 0
