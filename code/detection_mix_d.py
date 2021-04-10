import cv2
import numpy as np
import matplotlib.pyplot as plt

# hyper parameters
parameter1 = 50
parameter21 = 30
parameter22 = 40
min_distance = 80
min_radius = 20
max_radius = 40
min_offset = 10
max_offset = 20

# pre process image
img = cv2.imread('../data/top/no_background/004/front.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (3, 3))

# detects circles
detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 
    1, min_distance, param1 = parameter1, param2 = parameter21, minRadius = min_radius, maxRadius = max_radius)

# find median radius of circles
num_circles = detected_circles.shape[1]
sorted_circles = np.sort(detected_circles[0,:,2])
med_rad = int(sorted_circles[int(num_circles/2)])

# redetect circles with better radius parameter
min_rad = med_rad - min_offset
max_rad = med_rad + max_offset
detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 
    1, min_distance, param1 = parameter1, param2 = parameter22, minRadius = min_rad, maxRadius = max_rad)

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

cv2.line(img, (x_min, y_max), (x_min, y_min), (255, 255, 255), 2)
cv2.line(img, (x_min, y_max), (x_max, y_max), (255, 255, 255), 2)
cv2.line(img, (x_min, y_min), (x_max, y_min), (255, 255, 255), 2)
cv2.line(img, (x_max, y_min), (x_max, y_max), (255, 255, 255), 2)

x_step = (x_max - x_min) / 10
y_step = (y_max - y_min) / 10
for i in range(1):
    cv2.line(img, (int(x_min + x_step*i), y_max), (int(x_min + x_step*i), y_min), (255, 255, 255), 2)
    cv2.line(img, (x_min, int(y_min + y_step*i)), (x_max, int(y_min + y_step*i)), (255, 255, 255), 2)

# show circles on image
for pt in detected_circles[0,:]:
    a, b, r = int(pt[0]), int(pt[1]), int(pt[2])
    cv2.circle(img, (a,b), r, (0, 255, 0), 2)
    cv2.circle(img, (a,b), 1, (0, 0, 255), 3)
cv2.imshow("Detected Circles", img)

# press escape to get out of image window or your terminal might bug out
key = cv2.waitKey(0)
if key == 27:
    cv2.destroyAllWindows()