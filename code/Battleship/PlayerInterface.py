import cv2
import numpy as np
from colorama import init 
from termcolor import colored 
import copy
import math
import matplotlib.pyplot as plt

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
        self.vc = 0
    
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
        np.where(board == 1, colored("X", 'grey' ,'on_white'), colored("X", 'grey' ,'on_red')))
        s = ""
        alph = 65
        print("  12345678910")
        print(" ")
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
        np.where(board == 1, colored("X", 'grey' ,'on_white'), 
        np.where(board == 2, colored("O", 'white' ,'on_grey'), colored("X", 'grey' ,'on_red'))))
        s = ""
        alph = 65
        print("  12345678910")
        print(" ")
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
            print("Place your piece to continue!")
            _, img = self.vc.read()
            current_board = self.getBoardFromImage(img)
            if current_board == 0:
                print("Cannot find board!")
            while (not np.equal(self.opp_board, current_board)):
                _, img = self.vc.read()
                current_board = self.getBoardFromImage(img)
            return 0
        else:
            return 0

    def initialize_camera(self, whichplayer):
        self.use_camera = 1
        self.vc = cv2.VideoCapture(whichplayer)
        if not self.vc.isOpened():
            print( "No camera found or error opening camera; Using no camera option for player {}".format(whichplayer + 1))
            self.use_camera = 0


    # Returns a board state corresponding to the input image.
    # If no circles are detected in the image it will return 0.
    def getBoardFromImage(self, image):
        plt.imshow(image)
        plt.show()
        # adjustable parameters
        parameter1 = 50
        parameter21 = 30
        parameter22 = 40
        min_distance = 60
        min_radius = 20
        max_radius = 40
        min_offset = 10
        max_offset = 20
        target_image_size = 2000.0

        # pre process image
        scale_percent = target_image_size/image.shape[1]
        width = int(image.shape[1] * scale_percent)
        height = int(image.shape[0] * scale_percent)
        img = cv2.resize(image,(width, height))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.blur(gray, (3, 3))

        # detect the holes and pegs in the image, returns 0 if no circles are found
        detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 
            1, min_distance, param1 = parameter1, param2 = parameter21, minRadius = min_radius, maxRadius = max_radius)
        if detected_circles is None:
            return 0
        num_circles = detected_circles.shape[1]
        sorted_circles = np.sort(detected_circles[0,:,2])
        med_rad = int(sorted_circles[int(num_circles/2)])
        min_rad = med_rad - min_offset
        max_rad = med_rad + max_offset
        detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 
            1, min_distance, param1 = parameter1, param2 = parameter22, minRadius = min_rad, maxRadius = max_rad)
        if detected_circles is None:
            return 0

        # find corners of the grid using the detected circles
        num_circles = detected_circles.shape[1]
        av_x = 0
        av_y = 0
        for pt in detected_circles[0,:]:
            av_x += pt[0]
            av_y += pt[1]
        av_x = int(av_x/num_circles)
        av_y = int(av_y/num_circles)
        distances = np.zeros(num_circles)
        for i in range(num_circles):
            pt = detected_circles[0,i]
            distances[i] = math.sqrt(((av_x - pt[0]) ** 2) + ((av_y - pt[1]) ** 2))
        distances_indices = np.argsort(distances)
        closest_pts = np.zeros((4,2))
        center_x = 0
        center_y = 0
        for i in range(4):
            closest_pts[i,0] = detected_circles[0,distances_indices[i]][0]
            closest_pts[i,1] = detected_circles[0,distances_indices[i]][1]
            center_x += closest_pts[i,0]
            center_y += closest_pts[i,1]
        center_x = center_x / 4
        center_y = center_y / 4
        x_step = int(2 * np.amin(np.absolute(closest_pts[:,0] - center_x))) + 5
        y_step = int(2 * np.amin(np.absolute(closest_pts[:,1] - center_y))) + 5
        x_min = int(center_x - (5 * x_step))
        y_min = int(center_y - (5 * y_step))

        # calculate board representation from the calculated grid
        board = np.zeros((10,10))
        for i in range(10):
            for j in range(10):
                x_left = int(x_min + x_step*j)
                x_right = int(x_left + x_step)
                y_up = int(y_min + y_step*i)
                y_down = int(y_up + y_step)
                circle = False
                for pt in detected_circles[0,:]:
                    a, b, r = int(pt[0]), int(pt[1]), int(pt[2])
                    if x_left <= a <= x_right and y_up <= b <= y_down:
                        circle = True
                        ba = a
                        bb = b
                        br = r
                if circle == True:
                    red_window = img[bb-br:bb+br,ba-br:ba+br,2]
                    window = img[bb-br:bb+br,ba-br:ba+br,:]
                else:
                    offset_x = int(x_step/3)
                    offset_y = int(y_step/3)
                    red_window = img[y_up+offset_y:y_down-offset_y,x_left+offset_x:x_right-offset_x,2]
                    window = img[y_up+offset_y:y_down-offset_y,x_left+offset_x:x_right-offset_x,:]
                value = int(np.mean(window))
                red_value = int(np.mean(red_window))
                if value > 150:
                    board[i,j] = 1
                elif red_value > 175:
                    board[i,j] = 2
                else:
                    board[i,j] = 0
        
        return board
