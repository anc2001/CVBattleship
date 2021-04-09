import cv2
import numpy as np
import matplotlib.pyplot as plt

# hyper parameters
parameter1 = 50
parameter21 = 30
parameter22 = 40
min_distance = 80
min_radius = 10
max_radius = 40
min_offset = 5
max_offset = 10

# pre process image
img = cv2.imread('../data/top/no_background/001/front.png')
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
