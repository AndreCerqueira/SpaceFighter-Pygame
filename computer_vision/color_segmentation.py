import cv2
import numpy as np

# HSV color range values for red
hmin_red1, hmax_red1 = 0, 10
hmin_red2, hmax_red2 = 160, 180
smin_red, smax_red = 130, 255
vmin_red, vmax_red = 120, 255

# HSV color range values for green
hmin_green, hmax_green = 35, 85
smin_green, smax_green = 50, 255
vmin_green, vmax_green = 50, 255

def update_segmentation_red(image_hsv):
    # Create masks for red color detection and find contours
    mask_h1 = cv2.inRange(image_hsv[:, :, 0], hmin_red1, hmax_red1)
    mask_h2 = cv2.inRange(image_hsv[:, :, 0], hmin_red2, hmax_red2)
    mask_h = cv2.bitwise_or(mask_h1, mask_h2)
    mask_s = cv2.inRange(image_hsv[:, :, 1], smin_red, smax_red)
    mask_v = cv2.inRange(image_hsv[:, :, 2], vmin_red, vmax_red)
    mask = cv2.bitwise_and(mask_h, cv2.bitwise_and(mask_s, mask_v))
    cv2.imshow("Mask Red", mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        return cv2.boundingRect(largest_contour)
    else:
        return None

def update_segmentation_green(image_hsv):
    # Create masks for green color detection and find contours
    mask_h = cv2.inRange(image_hsv[:, :, 0], hmin_green, hmax_green)
    mask_s = cv2.inRange(image_hsv[:, :, 1], smin_green, smax_green)
    mask_v = cv2.inRange(image_hsv[:, :, 2], vmin_green, vmax_green)
    mask = cv2.bitwise_and(mask_h, cv2.bitwise_and(mask_s, mask_v))
    cv2.imshow("Mask Green", mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        return cv2.boundingRect(largest_contour)
    else:
        return None
