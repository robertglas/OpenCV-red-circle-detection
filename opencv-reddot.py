"""
Python port of Detect red circles in an image using OpenCV, for more informations visit the project webpage:

https://solarianprogrammer.com/2015/05/08/detect-red-circles-image-using-opencv/

Copyright 2015 Sol from www.solarianprogrammer.com
Pythn
"""
import cv2
import os
import sys


def check_if_image_exist(path):
    if not os.path.isfile(path):
        print("Error! Unable to load image: %s" % path)
        exit()


if len(sys.argv) != 2:
    print("Error! Program usage:")
    print("python opencv-reddot.py <image_circles_path>")
    exit()

# Load input image
path_image = sys.argv[1]
bgr_image = cv2.imread(path_image)

# Check if the image can be loaded
check_if_image_exist(path_image)

orig_image = bgr_image.copy()
bgr_image = cv2.medianBlur(bgr_image, 3)

# Convert input image to HSV
hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

# Threshold the HSV image, keep only the red pixels
lower_red_hue_range = cv2.inRange(hsv_image, (0, 100, 100), (10, 255, 255))
upper_red_hue_range = cv2.inRange(hsv_image, (160, 100, 100), (179, 255, 255))

# Combine the above two images
red_hue_image = cv2.addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0)
red_hue_image = cv2.GaussianBlur(red_hue_image, (9, 9), 2, 2)

# Use the Hough transform to detect circles in the combined threshold image
circles = cv2.HoughCircles(red_hue_image, cv2.HOUGH_GRADIENT, 1, red_hue_image.shape[0] / 8.0, 100, 20, 1, 1)

# Loop over all detected circles and outline them on the original image
if circles is None or len(circles) == 0:
    print('No circles were found! Exiting.')
    exit()
for current_circle in circles[0,:]:
    center = (int(current_circle[0]), int(current_circle[1]))
    radius = int(current_circle[2])
    cv2.circle(orig_image, center, radius, (0, 255, 0), 5)

# Show images
cv2.namedWindow("Threshold lower image", cv2.WINDOW_AUTOSIZE)
cv2.imshow("Threshold lower image", lower_red_hue_range)
cv2.namedWindow("Threshold upper image", cv2.WINDOW_AUTOSIZE)
cv2.imshow("Threshold upper image", upper_red_hue_range)
cv2.namedWindow("Combined threshold images", cv2.WINDOW_AUTOSIZE)
cv2.imshow("Combined threshold images", red_hue_image)
cv2.namedWindow("Detected red circles on the input image", cv2.WINDOW_AUTOSIZE)
cv2.imshow("Detected red circles on the input image", orig_image)
print('Now showing the results in openCV windows. Press any key to exit.')

cv2.waitKey(0)
