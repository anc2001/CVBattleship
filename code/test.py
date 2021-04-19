import numpy as np
import cv2 
import matplotlib.pyplot as plt
import os
import copy

# for i in range(8):
#     markerImage = cv2.aruco.drawMarker(dictionary, i, 70, 1)
#     cv2.imwrite("{}.png".format(i), markerImage)

vc = cv2.VideoCapture(0)
if not vc.isOpened():
    print( "No camera found or error opening camera; Using no camera option for player {}")

_,image = vc.read()
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100)
parameters = cv2.aruco.DetectorParameters_create()

# image = cv2.imread("../data/yay.png")

markerCorners, markerIds, _ = cv2.aruco.detectMarkers(image, dictionary, parameters=parameters)

outputimage = copy.deepcopy(image)
cv2.aruco.drawDetectedMarkers(outputimage, markerCorners, markerIds)
plt.imshow(outputimage)
plt.show()

markerCorners = [m[0] for m in markerCorners]

corners = []
for array in markerCorners:
    point = np.sum(array, axis=0)
    corners.append((int(point[0] / 4), int(point[1] / 4)))

dtype = [('x', int), ('y', int)]
corners = np.array(corners, dtype=dtype)
corners = np.sort(corners, order='y')

top_coords = corners[0:4]
bottom_coords = corners[-4:]

#Array inputis unordered
def perspective_transform(img, array):
    # top_left, top_right, bottom_left, bottom_right = [495, 179], [1693, 162], [552, 1319], [1664, 1300] # top/no_background/004/front
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

    plt.subplot(121),plt.imshow(img),plt.title('Input')
    plt.subplot(122),plt.imshow(dst),plt.title('Output')
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()

perspective_transform(image, top_coords)
perspective_transform(image, bottom_coords)

# for array in corners:
#     cv2.circle(image, (array[0],array[1]), radius=0, color=(0, 255, 0), thickness=-1)

# corners = np.sort(corners)
# print(corners)
# plt.imshow(image)
# plt.show()