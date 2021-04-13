import cv2
import numpy as np
import math

class Referee:
    def __init__(self, Player1, Player2):
        self.player1 = Player1
        self.player2 = Player2
        self.isplayer1 = 1
    
    def other_player(self, Player):
        if(Player == self.player1):
            return self.player2
        else :
            return self.player1
    
    def play_game(self):
        pass


    """
    Returns a board state corresponding to the input image.
    If no circles are detected in the image it will return 0.
    """
    def getBoardFromImage(self, image):
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
        x_step = int(2 * abs(center_x - np.amax(closest_pts[:,0])))
        y_step = int(2 * abs(center_y - np.amax(closest_pts[:,1])))
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