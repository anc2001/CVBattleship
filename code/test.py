import cv2 
import os
import numpy as np
from numpy import pi, exp, sqrt
from skimage import io, img_as_float32, img_as_ubyte
from skimage.color import rgb2gray
import matplotlib.pyplot as plt

image = cv2.imread('../data/bottom/first_setup/004/bottom_sparse.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray,(15,15),0)
thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
thresh = cv2.bitwise_not(thresh)
plt.imshow(thresh)
plt.show()