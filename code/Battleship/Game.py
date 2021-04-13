from Referee import Referee
from Human import Human
from AI import AI
import argparse
import random

def parse_args():
    parser = argparse.ArgumentParser(
        description="Let's play Battleship",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--playermode',
        required=True,
        choices=['hvh', 'hva', 'ava'],
        help='''hvh - human vs human, hva - human vs ai, ava - ai vs ai''')
    parser.add_argument(
        '--player1',
        required=False,
        help='''Player 1 name if human player''')
    parser.add_argument(
        '--player2',
        required=False,
        help='''Player 2 name if human player''')


    return parser.parse_args()

class Player(object):
    def __init__(self, name):
        self.name = name

class HumanPlayer(Player):
    def __init__(self, name):
        super(HumanPlayer, self).__init__(name)

    # possible implementation - not sure
    # def play(self, state, actions):
    #     while True:
    #         move = raw_input(self.name + ", please enter a move: ")
    #         if move not in actions:
    #             print("That move is not available. Try again!")
    #         else:
    #             return move

class AIPlayer(Player):
    def __init__(self, name):
        super(AIPlayer, self).__init__(name)
        
    # possible implementation - not sure
    def play(self, state, actions):
        return random.choice(actions)

def main():
    args = parse_args()
    if(args.playermode == "hvh"):
        player1 = args.player1
        player2 = args.player2
        if not(args.player1):
            player1 = "player1"
        if not(args.player2):
            player2 = "player2"
        Referee(HumanPlayer(player1), HumanPlayer(player2))
    elif (args.playermode == "hva"):
        player1 = ""
        if not(args.player1):
            player1 = "player1"
        Referee(HumanPlayer(player1), AIPlayer("ai"))
    elif (args.playermode == "ava"):
        Referee(AIPlayer("ai1"), AIPlayer("ai2"))



# Make arguments global
ARGS = parse_args()

main()