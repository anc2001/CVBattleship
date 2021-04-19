import numpy as np
import math

class Referee:
    def __init__(self, Player1, Player2):
        self.player1 = Player1
        self.player2 = Player2
        self.isplayer1 = 1
    
    def other_player(self):
        if(self.isplayer1):
            return self.player2
        else :
            return self.player1
    
    def play_game(self):
        current_player = self.player1
        names = ["Player 1", "Player 2"]
        move = ""
        while(not current_player.has_lost()):
            print("It's {}'s turn after receiving {}".format(names[not self.isplayer1], move))
            current_player.show_opp_board()
            print(" ")
            current_player.show_own_board()
            move = current_player.suggest_turn()
            hit_or_miss = self.other_player().receive_turn(move)
            while(not hit_or_miss): 
                print("Invalid Move! Try again!")
                move = current_player.suggest_turn()
                hit_or_miss = self.other_player().receive_turn(move)
            if hit_or_miss == 1:
                print("{} misses with move {}".format(names[not self.isplayer1], move))
                current_player.make_turn(move + "M")
            else:
                print("{} hits with move {}".format(names[not self.isplayer1], move))
                current_player.make_turn(move + "H")
            current_player = self.other_player()
            self.isplayer1 = not self.isplayer1
        print("{} has lost!".format(names[not self.isplayer1]))
        
