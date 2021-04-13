from Referee import Referee
from Human import Human
from AI import AI
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Let's play Battleship",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--task',
        required=True,
        choices=['1', '3'],
        help='''Which task of the assignment to run -
        training from scratch (1), or fine tuning VGG-16 (3).''')

    return parser.parse_args()

def main():
    pass

# Make arguments global
ARGS = parse_args()

main()