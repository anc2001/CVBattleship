import numpy as np
from PlayerInterface import PlayerInterface

class Human(PlayerInterface):
    #Constructor for human, poll in terminal for input starting positions
    def __init__(self):
        super(Human, self).__init__()

    #Takes in 10 x 10 and ignores it because this is a human, they have the 
    #board in front of them. Polls in terminal for the human to give their turn
    def suggest_turn(self, array):
        pass
    
