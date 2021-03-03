import numpy as np
import cv2 


class ThresholdWindow:

    def _check_max(self, id):
        return lambda x : cv2.setTrackbarPos(id, self._window_name, max(x, cv2.getTrackbarPos(id, self._window_name)))

    def _check_min(self, id):
        return lambda x : cv2.setTrackbarPos(id, self._window_name, min(x, cv2.getTrackbarPos(id, self._window_name)))  

    def __init__(self, name):
        self._window_name = name
        cv2.namedWindow(self._window_name)
        cv2.createTrackbar('Min Hue', self._window_name, 0, 360, self._check_max('Max Hue'))
        cv2.createTrackbar('Max Hue', self._window_name, 0, 360, self._check_min('Min Hue'))
        cv2.createTrackbar('Min Sat', self._window_name, 0, 255, self._check_max('Max Sat'))
        cv2.createTrackbar('Max Sat', self._window_name, 0, 255, self._check_min('Min Sat'))
        cv2.createTrackbar('Min Val', self._window_name, 0, 255, self._check_max('Max Val'))
        cv2.createTrackbar('Max Val', self._window_name, 0, 255, self._check_min('Min Val'))
    
    def min_thresholds(self):
        return (
            cv2.getTrackbarPos('Min Hue', self._window_name), 
            cv2.getTrackbarPos('Min Sat', self._window_name), 
            cv2.getTrackbarPos('Min Val', self._window_name)
        )
        
    def max_thresholds(self):
        return (
            cv2.getTrackbarPos('Max Hue', self._window_name), 
            cv2.getTrackbarPos('Max Sat', self._window_name), 
            cv2.getTrackbarPos('Max Val', self._window_name)
        )

    def imshow(self, img):
        cv2.imshow(self._window_name, img)

    def is_open(self):
        return cv2.getWindowProperty(self._window_name, 0) >= 0
