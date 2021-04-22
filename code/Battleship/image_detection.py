import cv2
import numpy as np
import math

# hyper parameters
parameter1 = 50
parameter21 = 30
parameter22 = 40
min_distance = 80
min_radius = 20
max_radius = 40
min_offset = 10
max_offset = 20
target_image_size = 2000.0

# pre process image
img = cv2.imread('../data/top/custom_background/003.png')
img = np.array(img)
scale_percent = target_image_size/img.shape[1]
width = int(img.shape[1] * scale_percent)
height = int(img.shape[0] * scale_percent)
img = cv2.resize(img,(width, height))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (3, 3))

# detect circles
detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 
    1, min_distance, param1 = parameter1, param2 = parameter21, minRadius = min_radius, maxRadius = max_radius)
if detected_circles is None:
    print("No circles were detected in the image")
num_circles = detected_circles.shape[1]
sorted_circles = np.sort(detected_circles[0,:,2])
med_rad = int(sorted_circles[int(num_circles/2)])
min_rad = med_rad - min_offset
max_rad = med_rad + max_offset
detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 
    1, min_distance, param1 = parameter1, param2 = parameter22, minRadius = min_rad, maxRadius = max_rad)
if detected_circles is None:
    print("No circles were detected in the image")
for pt in detected_circles[0,:]:
    a, b, r = int(pt[0]), int(pt[1]), int(pt[2])
    cv2.circle(img, (a,b), r, (0, 255, 0), 2)
    cv2.circle(img, (a,b), 1, (0, 0, 255), 3)

# find corners of the grid
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
x_max = int(center_x + (5 * x_step))
y_min = int(center_y - (5 * y_step))
y_max = int(center_y + (5 * y_step))
cv2.line(img, (x_min, y_max), (x_min, y_min), (255, 255, 255), 2)
cv2.line(img, (x_min, y_max), (x_max, y_max), (255, 255, 255), 2)
cv2.line(img, (x_min, y_min), (x_max, y_min), (255, 255, 255), 2)
cv2.line(img, (x_max, y_min), (x_max, y_max), (255, 255, 255), 2)

# calculate board representation from current grid
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

# visualize the board
scale_percent = 800.0/img.shape[0]
width = int(img.shape[1] * scale_percent)
height = int(img.shape[0] * scale_percent)
shrink = cv2.resize(img,(width, height))
canvas = np.full((800,800,3),.1)
for i in range(10):
    for j in range(10):
        start = (40 + 80*j,40 + 80*i)
        if board[i,j] == 1:
            cv2.circle(canvas, start, 35, (.75, .75, .75), -1)
        elif board[i,j] == 2:
            cv2.circle(canvas, start, 35, (.1, .1, .75), -1)
        else:
            cv2.circle(canvas, start, 35, (.5, .1, .1), -1)
cv2.imshow("Detected Circles/Board", shrink)
cv2.imshow("Board Evaluation", canvas)
key = cv2.waitKey(0)
if key == 27:
    cv2.destroyAllWindows()
