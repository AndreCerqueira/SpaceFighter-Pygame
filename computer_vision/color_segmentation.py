import cv2
import numpy as np

# Valores HSV para face amarela
hmin_yellow, hmax_yellow = 20, 40
smin_yellow, smax_yellow = 50, 255
vmin_yellow, vmax_yellow = 50, 255

# Valores HSV para face vermelha
hmin_red1, hmax_red1 = 0, 10
hmin_red2, hmax_red2 = 160, 180
smin_red, smax_red = 50, 255
vmin_red, vmax_red = 50, 255

# Valores HSV para face verde
hmin_green, hmax_green = 35, 85
smin_green, smax_green = 50, 255
vmin_green, vmax_green = 50, 255

def update_segmentation_yellow(image_hsv):
    mask_h = cv2.inRange(image_hsv[:, :, 0], hmin_yellow, hmax_yellow)
    mask_s = cv2.inRange(image_hsv[:, :, 1], smin_yellow, smax_yellow)
    mask_v = cv2.inRange(image_hsv[:, :, 2], vmin_yellow, vmax_yellow)

    mask = cv2.bitwise_and(mask_h, cv2.bitwise_and(mask_s, mask_v))
    cv2.imshow("Mask Yellow", mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x + w // 2, y + h // 2, w, h
    else:
        return None

def update_segmentation_red(image_hsv):
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
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x + w // 2, y + h // 2, w, h
    else:
        return None

def update_segmentation_green(image_hsv):
    mask_h = cv2.inRange(image_hsv[:, :, 0], hmin_green, hmax_green)
    mask_s = cv2.inRange(image_hsv[:, :, 1], smin_green, smax_green)
    mask_v = cv2.inRange(image_hsv[:, :, 2], vmin_green, vmax_green)

    mask = cv2.bitwise_and(mask_h, cv2.bitwise_and(mask_s, mask_v))
    cv2.imshow("Mask Green", mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x + w // 2, y + h // 2, w, h
    else:
        return None

