import cv2
import numpy as np
import matplotlib.pyplot as plt

# pre process image
img = cv2.imread('../data/top/no_background/004/front.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (10, 10))

# detect circles (parameters tuned by me, not sure how we could come up with them using code)
detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 
    1, 85, param1 = 50, param2 = 40, minRadius = 10, maxRadius = 40)

# find median radius
num_circles = detected_circles.shape[1]
sorted_circles = np.sort(detected_circles[0,:,2])
med_rad = int(sorted_circles[int(num_circles/2)])

# detect circles with new radius range to get rid of outliers
min_rad = med_rad - 5
max_rad = med_rad + 20
detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 
    1, 85, param1 = 50, param2 = 40, minRadius = min_rad, maxRadius = max_rad)

# show circles on image
for pt in detected_circles[0,:]:
    a, b, r = int(pt[0]), int(pt[1]), int(pt[2])
    cv2.circle(img, (a,b), r, (0, 255, 0), 2)
    cv2.circle(img, (a,b), 1, (0, 0, 255), 3)

# press escape to get out of image window or your terminal might bug out
cv2.imshow("Detected Circles", img)
key = cv2.waitKey(0)
if key == 27:
    cv2.destroyAllWindows()
