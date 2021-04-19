import cv2
import numpy as np
import matplotlib.pyplot as plt

#Hyperparameters to calibrate 
#Should be a positive value
height_head = 20

#Should be a negative value
height_feet = -30

#Should be a positive value
width_left = 60

#If needed, can include
width_right = 0


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

    plt.imshow(img)
    plt.show()

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
            plt.imshow(window)
            plt.show()
            value = int(np.mean(window))
            red_value = int(np.mean(red_window))
            if value > 150:
                board[i,j] = 1
            elif red_value > 175:
                board[i,j] = 2
            else:
                board[i,j] = 0
        
    return board

vc = cv2.VideoCapture(0)
_,img = vc.read()
corners = get_aruco(img)

if len(corners) == 0:
    print("Cannot find board")
else:
    top_img = perspective_transform(img, corners[0:4])
    current_board = getBoardFromImage(top_img)