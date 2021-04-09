import cv2
import numpy as np
import matplotlib.pyplot as plt

# pre process image
img = cv2.imread('../data/top/no_background/004/front.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (3, 3))

# detect circles (parameters tuned by me, not sure how we could come up with them using code)
detected_circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 
    1, 85, param1 = 50, param2 = 40, minRadius = 10, maxRadius = 40)

# here I plan on getting rid of the outliers (just calculates centroid rn)
num_pts = detected_circles.shape[1]
a_av = 0
b_av = 0
for pt in detected_circles[0,:]:
    a_av += int(pt[0])
    b_av += int(pt[1])
a_av = a_av/num_pts
a_av = a_av/num_pts
centroid = (a_av,b_av)

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
