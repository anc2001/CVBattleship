import cv2
import numpy as np
import matplotlib.pyplot as plt

# pre process image
img = cv2.imread('../data/ah.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (3, 3))

x,y,w,h = cv2.boundingRect(blur)
cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

# detect circles (parameters tuned by me, not sure how we could come up with them using code)
detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 
    1, 85, param1 = 50, param2 = 40, minRadius = 1, maxRadius = 40)

# Methodology - want to estimate corners from detected points, know they're evenly spaced so
num_pts = detected_circles.shape[1]
xs = np.array([])
ys = np.array([])
for pt in detected_circles[0,:]:
    xs = np.append(xs, [pt[0]])
    ys = np.append(ys, [pt[1]])

sample_size = 10
xs = np.sort(xs)
ys = np.sort(ys)
x_min = int(np.average(xs[0:sample_size]) + 20)
x_max = int(np.average(xs[-sample_size:]) + 20)
y_min = int(np.average(ys[0:sample_size]) + 40)
y_max = int(np.average(ys[-sample_size:]) + 40)

x_step = (x_max - x_min) / 10
y_step = (y_max - y_min) / 10

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

print(board)