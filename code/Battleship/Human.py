import numpy as np
from PlayerInterface import PlayerInterface

class Human(PlayerInterface):
    # Constructor for human, poll in terminal for input starting positions
    def __init__(self):
        super(Human, self).__init__()
        # Battleship terminal stuff
        self.battleships = self.place_battleships()
        self.set_own_board()
        self.use_camera = 0

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
        return 0

    # Print battleship board
    def print_board(self, battleship_info):
        board = np.zeros((10, 10))
        for (row, col, orientation, size) in battleship_info:
            coordinates = self.info_to_coordinates(row, col, orientation, size)
            for coordinate in coordinates:
                row, col = ord(coordinate[0]) - 65, int(coordinate[1]) - 1
                board[row][col] = 1
        print(board)
        return board


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

    # Returns whether or not there is a conflict when adding a battleship to a coordinate
    def conflict_exists(self, battleship_info, row, col, orientation, size):
        if ((orientation == 'up' and ord(row) - 64 - size < 0) or 
            (orientation == 'down' and ord(row) - 64 + size > 11) or 
            (orientation == 'left' and int(col) + size < 0) or 
            (orientation == 'right' and int(col) + size > 11)):
            return True

        for (ship_row, ship_col, ship_orientation, ship_size) in battleship_info:
            ship_coordinates = self.info_to_coordinates(ship_row, ship_col, ship_orientation, ship_size)
            curr_coordinates = self.info_to_coordinates(row, col, orientation, size)

            if not set(ship_coordinates).isdisjoint(curr_coordinates):
                return True
        return False
    
    # Prompts user to place 5 battleships on a 10x10 grid. 
    # Returns an array of battleship info that is 5 x 4 with each inner array being in format: [row, column, ship orientation, ship size]
    def place_battleships(self):
        battleships = [
            ['Patrol Boat', 2], 
            ['Submarine', 3],
            ['Destroyer', 3],
            ['Battleship', 4],
            ['Carrier', 5]
        ]
        battleship_info = []

        for index, (ship_name, ship_size) in enumerate(battleships):
            print("Place your '{}' piece of size {}.".format(ship_name, ship_size))

            # Row input
            row = input("Row (A-J): ").upper()
            while len(row) != 1 or not row.isalpha() or not row in "ABCDEFGHIJ":
                row = input("Please enter a letter (A-J) indicating the row of where you'd like to place your {} piece: ".format(ship_name)).upper()
            
            # Column input
            col = input("Column (1-10): ")
            while col != '10' and (len(col) != 1 or not col.isnumeric()):
                col = input("Please enter a number (1-10) indicating the column of where you'd like to place your {} piece: ".format(ship_name))

            # Edge case where other battleships surround input coordinate
            while (
                self.conflict_exists(battleship_info, row, col, 'up', ship_size) and 
                self.conflict_exists(battleship_info, row, col, 'down', ship_size) and
                self.conflict_exists(battleship_info, row, col, 'right', ship_size) and
                self.conflict_exists(battleship_info, row, col, 'left', ship_size)
                ):
                print("Invalid coordinate detected. Please re-enter another set of coordinates.")

                row = input("Row (A-J): ").upper()
                while len(row) != 1 or not row.isalpha() or not row in "ABCDEFGHIJ":
                    row = input("Please enter a letter (A-J) indicating the row of where you'd like to place your {} piece: ".format(ship_name)).upper()
                
                col = input("Column (1-10): ")
                while col != '10' and (len(col) != 1 or not col.isnumeric()):
                    col = input("Please enter a number (1-10) indicating the column of where you'd like to place your {} piece: ".format(ship_name))
            
            # Orientation input + Conflict checker
            orientation = input("Orientation (up, down, left, right): ").lower()
            while (
                (orientation != 'up' and orientation != 'down' and orientation != 'left' and orientation != 'right') or 
                self.conflict_exists(battleship_info, row, col, orientation, ship_size)
            ):
                orientation = input("Please enter a valid orientation (up, down, left, right) " +
                "that doesn't go out of bounds and doesn't overlap with your other battleships: ").lower()
            
            battleship_info.append([row, col, orientation, ship_size])

        self.print_board(battleship_info)

        return battleship_info

    # Polls in terminal for the human to give their turn. array input is not used.
    def suggest_turn(self, array):
        # Get row for move
        player_row = input("Enter the row of your move (A-J): ").upper()
        while len(player_row) != 1 or not player_row.isalpha() or not player_row in "ABCDEFGHIJ":
            player_row = input("Please enter a letter (A-J) indicating the row of your move (A-J): ").upper()
        
        # Get column for move
        player_col = input("Enter the column of your move (1-10): ")
        while player_col != '10' and (len(player_col) != 1 or not player_col.isnumeric()):
            player_col = input("Please enter a number (1-10) indicating the column of your move (1-10): ")
        
        return player_row + player_col

Human().place_battleships()