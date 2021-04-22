import cv2
import numpy as np 
from termcolor import colored 
import copy
import math
import matplotlib.pyplot as plt
from skimage import feature
from skimage.color import rgb2gray
import calibrate

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
        #Aruco stuff
        self.vc = 0
        self.dictionary = calibrate.dictionary
        self.parameters = calibrate.parameters
    
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

        def poll_for_change():
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

            if sunk: 
                print("You sunk one as well!")
                if self.use_camera:
                    poll_for_change()
                return 2
            else:
                if self.use_camera:
                    poll_for_change()
                return 2
        else:
            self.own_board[row][column] = 1
            print("Miss!")
            if self.use_camera:
                poll_for_change()
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
        
        def check_equality(current_board):
            if len(current_board) != 0:
                for i in range(10):
                    for j in range(10):
                        if self.opp_board[i][j] != current_board[i][j]:
                            return 1
                return 0
            else:
                return 1

        if self.use_camera:
            #Poll for confirmational change, wait until the board matches our board
            print("Place your piece to continue!. The piece to place is {}".format(move))
            _, img = self.vc.read()
            corners = self.get_aruco(img)
            current_board = np.random.rand(10,10)
            if len(corners):
                top_img = self.perspective_transform(img, corners[0:4])
                current_board = self.getBoardFromImage(top_img)
            while (check_equality(current_board)):
                _, img = self.vc.read()
                corners = self.get_aruco(img)
                if len(corners):
                    top_img = self.perspective_transform(img, corners[0:4])
                    current_board = self.getBoardFromImage(top_img)
            return 0
        else:
            return 0

    def initialize_camera(self, whichplayer):
        self.use_camera = 1
        self.vc = cv2.VideoCapture(whichplayer)
        if not self.vc.isOpened():
            print( "No camera found or error opening camera; Using no camera option for player {}".format(whichplayer + 1))
            self.use_camera = 0
    
    def get_aruco(self, image):
        markerCorners, _, _ = cv2.aruco.detectMarkers(image, self.dictionary, parameters=self.parameters)
        if len(markerCorners) < 4:
            return []
        
        markerCorners = [m[0] for m in markerCorners]
        corners = []
        for array in markerCorners:
            point = np.sum(array, axis=0)
            corners.append((int(point[0] / 4), int(point[1] / 4)))

        dtype = [('x', int), ('y', int)]
        corners = np.array(corners, dtype=dtype)
        corners = np.sort(corners, order='y')

        return corners
    
    #Array inputs unordered
    def perspective_transform(self, img, array):
        dtype = [('x', int), ('y', int)]
        first = np.array(array, dtype=dtype)
        first = np.sort(array, order='y')
        total = np.append(np.sort(first[0:2], order='x'), np.sort(first[-2:], order='x'))
        total = [[coord[0], coord[1]] for coord in total]
        top_left, top_right, bottom_left, bottom_right = total[0], total[1], total[2], total[3]
        x_size, y_size = img.shape[1], img.shape[0]

        inner_crop = np.float32([top_left, top_right, bottom_left, bottom_right])
        # inner_crop = corners
        outer_crop = np.float32([[0, 0], [x_size, 0], [0, y_size], [x_size, y_size]])

        M = cv2.getPerspectiveTransform(inner_crop, outer_crop)

        dst = cv2.warpPerspective(img, M, (x_size, y_size))

        return dst

    # Returns a board state corresponding to the input image.
    # If no circles are detected in the image it will return 0.
    def getBoardFromImage(self, image):
        img = np.array(image[calibrate.height_head:calibrate.height_feet,calibrate.width_left:,:])
        target_image_size = 1000.0
        scale_percent = target_image_size/img.shape[1]
        width = int(img.shape[1] * scale_percent)
        width = round(width/10)*10
        height = int(img.shape[0] * scale_percent)
        height = round(height/10)*10
        img = cv2.resize(img,(width, height))

        x_step = int(width / 10)
        y_step = int(height / 10)
        board = np.zeros((10,10))
        for i in range(10):
            for j in range(10):
                x_left = int(x_step*j)
                x_right = int(x_left + x_step)
                y_up = int(y_step*i)
                y_down = int(y_up + y_step)
                red_window = img[y_up:y_down,x_left:x_right,2]
                window = img[y_up:y_down,x_left:x_right,:]

                threshold = np.sqrt(x_step * y_step / (2 * 3 * np.pi))
                gray = rgb2gray(window)
                keypoints_white = feature.blob_dog(gray, min_sigma=threshold - 2, max_sigma=30)
                keypoints_red = feature.blob_dog(window[:,:,2], min_sigma=threshold - 2, max_sigma=30)

                white_flag = 0
                red_flag = 0
                for keypoint in keypoints_white:  
                    if keypoint[2] > threshold:
                        white_flag = 1
                for keypoint in keypoints_red:
                    if keypoint[2] > threshold:
                        red_flag = 1

                
                offset_x = int(x_step/3)    
                offset_y = int(y_step/3)
                sub_red_window = np.array(img[y_up+offset_y:y_down-offset_y,x_left+offset_x:x_right-offset_x,2])
                sub_window = np.array(img[y_up+offset_y:y_down-offset_y,x_left+offset_x:x_right-offset_x,:])

                white_inside_average = np.sum(sub_window) / np.prod(sub_window.shape)
                red_inside_average = np.sum(sub_red_window) / np.prod(sub_red_window.shape)
                white_outside_average = (np.sum(window) - np.sum(sub_window)) / (np.prod(window.shape) - np.prod(sub_window.shape))
                red_outside_average = (np.sum(red_window) - np.sum(sub_red_window)) / (np.prod(red_window.shape) - np.prod(sub_red_window.shape))

                white_difference = white_inside_average - white_outside_average
                red_difference = red_inside_average - red_outside_average
                white_color_flag = 0
                red_color_flag = 0
                if white_difference > 40:
                    white_color_flag = 1
                if red_difference > 40:
                    red_color_flag = 1

                if (white_flag and red_flag) or (white_color_flag):
                # print("Detected Miss")
                    board[i,j] = 1
                elif red_flag or (red_color_flag):
                # print("Detected Hit")
                    board[i,j] = 2
                else:
                # print("Detected nothing present")
                    board[i,j] = 0
        
        return board
