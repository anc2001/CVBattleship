import numpy as np
from PlayerInterface import PlayerInterface

class AI(PlayerInterface):
    # Constructor for human, poll in terminal for input starting positions
    def __init__(self):
        super(AI, self).__init__()

    # Takes in 10 x 10 board and suggests turn
    def suggest_turn(self, array):
        pass