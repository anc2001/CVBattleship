import numpy as np
from playerInterface import PlayerInterface

class AI(PlayerInterface):
    # Constructor for human, poll in terminal for input starting positions
    def __init__(self):
        super(AI, self).__init__()
        self.previousmoves = set()
        self.rows = np.array(['A','B','C','D','E','F','G','H','I','J'])
        self.cols = np.array(['1','2','3','4','5','6','7','8','9','10'])
        # if self.use_camera:
        #     self.battleships = self.place_battleships_camera()
        # else:
        #     self.battleships = self.place_battleships_random()
        self.battleships = self.place_battleships_random()
        self.set_own_board()

    # Randomly places 5 battleships on a 10x10 grid. 
    # Returns an array of battleship info that is 5 x 4 with each inner array being in format: [row, column, ship orientation, ship size]
    def place_battleships_random(self):
        battleships = [
            ['Patrol Boat', 2], 
            ['Submarine', 3],
            ['Destroyer', 3],
            ['Battleship', 4],
            ['Carrier', 5]
        ]
        battleship_info = []

        for index, (ship_name, ship_size) in enumerate(battleships):
            row = np.random.choice(self.rows)
            col = np.random.choice(self.cols)

            # Edge case where other battleships surround input coordinate
            while (
                self.conflict_exists(battleship_info, row, col, 'up', ship_size) and 
                self.conflict_exists(battleship_info, row, col, 'down', ship_size) and
                self.conflict_exists(battleship_info, row, col, 'right', ship_size) and
                self.conflict_exists(battleship_info, row, col, 'left', ship_size)
                ):
                row = np.random.choice(self.rows)
                col = np.random.choice(self.cols)
            
            # Orientation input + Conflict checker
            orientations = ['up', 'down', 'right', 'left']
            orientation = np.random.choice(orientations)
            while (self.conflict_exists(battleship_info, row, col, orientation, ship_size)):
                orientation = np.random.choice(orientations)
            
            battleship_info.append([row, col, orientation, ship_size])

        return battleship_info
    
    # Takes in 10 x 10 board and suggests turn
    def suggest_turn(self):
        row = np.random.choice(self.rows)
        col = np.random.choice(self.cols)
        move = row + col
        while self.previousmoves.__contains__(move):
            row = np.random.choice(self.rows)
            col = np.random.choice(self.cols)
            move = row + col
        self.previousmoves.add(move)
        return move