import cv2 
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Option 1: Detect features
def feature_detection(img, img_gray):
    # Grab features - https://docs.opencv.org/3.4/dd/d1a/group__imgproc__feature.html#ga1d6bb77486c8f92d79c8793ad995d541
    features = cv2.goodFeaturesToTrack(img_gray, maxCorners=1000, qualityLevel=0.05, minDistance=5)

    # Visualize features
    for i in features:
        x,y = i.ravel()
        cv2.circle(img, (x,y), 7, 255, -1)

    plt.imshow(img)
    plt.show()

def find_contours(img, img_gray, visualize=False):
    # Blur image using Gaussian
    blur = cv2.GaussianBlur(img_gray, (15,15), 0)

    # Find threshold of blur
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)

    # Find contours - https://docs.opencv.org/master/d4/d73/tutorial_py_contours_begin.html
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Create contoured_image
    copied_img = img.copy()
    copied_img.fill(255)
    cv2.drawContours(copied_img, contours, -1, (0, 0, 0), 5)

    # Visualize contours
    if visualize:
        plt.imshow(copied_img)
        plt.show()
    
    return copied_img, contours

def find_rectangles(img, contours, detect, visualize=False):
    rectangles = []
    img_area = np.product(img.shape)
    for cnt in contours:
        A = cv2.contourArea(cnt, False)
        p = cv2.arcLength(cnt, True)
        if p == 0:
            continue
        f_circ = (4 * np.pi * A) / (p ** 2)

        if f_circ > 0.5:
            epsilon = 0.04 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, False)
            area = cv2.contourArea(approx)
            rect = cv2.minAreaRect(approx)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            percentage = (area * 100) / img_area

            if detect == 'tile centers':
                if percentage > 0.001 and percentage < 0.005:
                    rectangles.append(box)
            elif detect == 'pins':
                if percentage > 0.02 and percentage < 0.08:
                    rectangles.append(box)
            elif detect == 'tile squares':
                if percentage > 0.8:
                    rectangles.append(box)
    
    # Visualize end result
    copied_img = img.copy()
    cv2.drawContours(copied_img, rectangles, -1, (255, 0, 0), 3)
    
    if visualize:
        plt.imshow(copied_img)
        plt.show()

    return copied_img

def perspective_transform(img):
    top_left, top_right, bottom_left, bottom_right = [490, 257], [1533, 260], [475, 1351], [1576, 1325]
    x_size, y_size = img.shape[1], img.shape[0]

    inner_crop = np.float32([top_left, top_right, bottom_left, bottom_right])
    outer_crop = np.float32([[0, 0], [x_size, 0], [0, y_size], [x_size, y_size]])

    M = cv2.getPerspectiveTransform(inner_crop, outer_crop)

    dst = cv2.warpPerspective(img, M, (x_size, y_size))

    plt.subplot(121),plt.imshow(img),plt.title('Input')
    plt.subplot(122),plt.imshow(dst),plt.title('Output')
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()

# Get directory of image
img_dir = Path('../data/top/no_background/000')

# For each image in the directory of type PNG
for img_path in img_dir.glob('*.png'):
    # Grab image
    img = cv2.imread(str(img_path))

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Different options

    # feature_detection(img, img_gray, True)

    # copied_img, contours = find_contours(img, img_gray, True)
    # copied_gray = cv2.cvtColor(copied_img, cv2.COLOR_BGR2GRAY)

    # find_rectangles(copied_img, contours, 'pins', True)

    perspective_transform(img)
    exit()

# mng = plt.get_current_fig_manager()
# mng.full_screen_toggle()