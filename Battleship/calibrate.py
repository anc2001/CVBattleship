import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import filters, feature
from skimage.color import rgb2gray

#Hyperparameters to calibrate 
#Should be a positive value
height_head = 20

#Should be a negative value
height_feet = -30

#Should be a positive value
width_left = 60

#If needed, can include
width_right = 0

detector = cv2.SimpleBlobDetector()

dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100)
parameters = cv2.aruco.DetectorParameters_create()
def get_aruco(image):
    markerCorners, _, _ = cv2.aruco.detectMarkers(image, dictionary, parameters=parameters)
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
def perspective_transform(img, array):
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
def getBoardFromImage(image):
    img = np.array(image[height_head:height_feet,width_left:,:])
    target_image_size = 1000.0
    scale_percent = target_image_size/img.shape[1]
    width = int(img.shape[1] * scale_percent)
    width = round(width/10)*10
    height = int(img.shape[0] * scale_percent)
    height = round(height/10)*10
    img = cv2.resize(img,(width, height))

    cv2.imshow('thing', img)
    key = cv2.waitKey(0)

    x_step = int(width / 10)
    y_step = int(height / 10)
    board = np.zeros((10,10))
    for i in range(10):
        for j in range(10):
            x_left = int(x_step*j)
            x_right = int(x_left + x_step)
            y_up = int(y_step*i)
            y_down = int(y_up + y_step)
            window = img[y_up:y_down,x_left:x_right,:]
            red_window = img[y_up:y_down,x_left:x_right,2]

            gray = rgb2gray(window)
            threshold = np.sqrt(x_step * y_step / (3 * 3 * np.pi))
            keypoints_white = feature.blob_dog(gray, min_sigma=threshold-1, max_sigma=30)
            # print(keypoints_white)
            keypoints_red = feature.blob_dog(window[:,:,2], min_sigma=threshold-1, max_sigma=30)
            # print(keypoints_red)

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

            # cv2.imshow("thing" ,window)
            # key = cv2.waitKey(0)

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

# vc = cv2.VideoCapture(0)
# _,img = vc.read()
# corners = get_aruco(img)

# if len(corners) == 0:
#     print("Cannot find board")
# else:
#     top_img = perspective_transform(img, corners[0:4])
#     current_board = getBoardFromImage(top_img)
#     print(current_board)