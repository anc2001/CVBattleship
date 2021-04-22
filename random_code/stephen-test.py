import cv2 
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

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

def get_corners(img):
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

    # cv2.line(img, (x_min, y_max), (x_min, y_min), (255, 0, 0), 2)
    # cv2.line(img, (x_min, y_max), (x_max, y_max), (255, 0, 0), 2)
    # cv2.line(img, (x_min, y_min), (x_max, y_min), (255, 0, 0), 2)
    # cv2.line(img, (x_max, y_min), (x_max, y_max), (255, 0, 0), 2)

    # Add error margin
    # x_min -= 50
    # y_min -= 50
    # x_max += 50
    # y_max += 50

    # Format corners
    corners = np.float32([[x_min, y_min], [x_max, y_min], [x_min, y_max], [x_max, y_max]])
    return corners

def detect_biggest_rect(img):
    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur image using Gaussian
    blur = cv2.GaussianBlur(img_gray, (15,15), 0)

    # Find threshold of blur
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Find top n largest area contours
    top_32 = np.zeros((32, 2))
    for idx in range(len(contours)):
        approx = cv2.approxPolyDP(contours[idx], 0.01 * cv2.arcLength(contours[idx], True), False)
        area = cv2.contourArea(approx, False)
        if np.min(top_32[:,0]) < area:
            index_to_replace = np.argmin(top_32[:, 0])
            top_32[index_to_replace] = [area, idx]
    
    results = np.array(contours)[np.uint8(top_32[:, 1])]

    # Create contoured_image
    cv2.drawContours(img, results, -1, (255, 0, 0), 5)
    plt.imshow(img)
    plt.show()

def perspective_transform(img, corners):
    # top_left, top_right, bottom_left, bottom_right = [495, 179], [1693, 162], [552, 1319], [1664, 1300] # top/no_background/004/front
    top_left, top_right, bottom_left, bottom_right = [757, 197], [1855, 246], [780, 1550], [1766, 1284] # top/no_background/004/left
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

# Get directory of image
img_dir = Path('../data/top/no_background/004')

# For each image in the directory of type PNG
for img_path in img_dir.glob('*.png'):
    # Grab image
    # img = cv2.imread(str(img_path))
    img = cv2.imread('../data/top/no_background/004/left.png')

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Different options

    # feature_detection(img, img_gray, True)

    # copied_img, contours = find_contours(img, img_gray, True)
    # copied_gray = cv2.cvtColor(copied_img, cv2.COLOR_BGR2GRAY)

    # find_rectangles(copied_img, contours, 'pins', True)

    perspective_transform(img, get_corners(img))

    # detect_biggest_rect(img)
    exit()

# mng = plt.get_current_fig_manager()
# mng.full_screen_toggle()