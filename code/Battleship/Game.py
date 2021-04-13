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


def main():
    args = parse_args()
    if(args.playermode == "hvh"):
        Referee(Human(), Human())
    elif (args.playermode == "hva"):
        Referee(Human(), AI())
    elif (args.playermode == "ava"):
        Referee(AI(), AI())



# Make arguments global
ARGS = parse_args()

main()