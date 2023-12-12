import cv2
import numpy as np
import time

def update_tracker_green(frame, tracker, green):
    success, bbox = tracker.update(frame)
    x_center = 0
    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        x_center = x + w // 2
        green.y = y + h // 2
    return x_center

def update_tracker_red(frame, tracker, red):
    success, bbox = tracker.update(frame)
    x_center = 0
    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        x_center = x + w // 2
        red.y = y + h // 2
    return x_center