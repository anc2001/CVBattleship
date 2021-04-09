import cv2
import numpy as np
import matplotlib.pyplot as plt

image  = cv2.imread("../data/bottom/first_setup/000/bottom_sparse.png")
cv2.imshow("Image", image)
cv2.waitKey(0)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray", gray)
cv2.waitKey(0)

blur = cv2.GaussianBlur(gray, (5,5), 0)
cv2.imshow("blur", blur)
cv2.waitKey(0)

thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
cv2.imshow("thresh", thresh)
cv2.waitKey(0)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

max_area = 0
c = 0
for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
                if area > max_area:
                    max_area = area
                    best_cnt = i
                    image = cv2.drawContours(image, contours, c, (0, 255, 0), 3)
        c+=1

mask = np.zeros((gray.shape),np.uint8)
cv2.drawContours(mask,[best_cnt],0,255,-1)
cv2.drawContours(mask,[best_cnt],0,0,2)
cv2.imshow("mask", mask)
cv2.waitKey(0)

out = np.zeros_like(gray)
out[mask == 255] = gray[mask == 255]
cv2.imshow("New image", out)
cv2.waitKey(0)

blur = cv2.GaussianBlur(out, (5,5), 0)
cv2.imshow("blur1", blur)
cv2.waitKey(0)

thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
cv2.imshow("thresh1", thresh)
cv2.waitKey(0)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

c = 0
for i in contours:
        area = cv2.contourArea(i)
        if area > 1000/2:
            cv2.drawContours(image, contours, c, (0, 255, 0), 3)
        c+=1


cv2.imshow("Final Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()