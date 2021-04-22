from referee import Referee
from human import Human
from ai import AI
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
        '--player1_usecamera',
        required=False,
        choices=['yes', 'no'],
        default= 'no',
        help='''If player1 is using a camera then yes''')
    parser.add_argument(
        '--player2_usecamera',
        required=False,
        choices=['yes', 'no'],
        default= 'no',
        help='''If player2 is using a camera then yes''')


    return parser.parse_args()


def main():
    args = parse_args()
    if(args.playermode == "hvh"):
        player1 = Human()
        if args.player1_usecamera == "yes":
            player1.initialize_camera(0)
        player2 = Human()
        if args.player2_usecamera == "yes":
            player2.initialize_camera(1)
        referee = Referee(player1, player2)
        referee.play_game()
    elif (args.playermode == "hva"):
        player1 = Human()
        if args.player1_usecamera == "yes":
            player1.initialize_camera(0)
        player2 = AI()
        if args.player2_usecamera == "yes":
            player2.initialize_camera(1)
        referee = Referee(player1, player2)
        referee.play_game()
    elif (args.playermode == "ava"):
        player1 = AI()
        if args.player1_usecamera == "yes":
            player1.initialize_camera(0)
        player2 = AI()
        if args.player2_usecamera == "yes":
            player2.initialize_camera(1)
        referee = Referee(player1, player2)
        referee.play_game()



# Make arguments global
ARGS = parse_args()

main()