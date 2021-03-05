import numpy as np
import cv2 

def nothing(x):
    pass

# Window that helps manage an OpenCV window and treshold values
class ThresholdWindow:

    # functions to get and set the values of trackbars
    def _get_bar(self, id):
        return cv2.getTrackbarPos(id, self._window_name)

    def _set_bar(self, id, value):
        return cv2.setTrackbarPos(id, self._window_name, value)

    # funtions that help the track bars stay linked with their related bars
    def _check_max(self, id):
        return lambda x : self._set_bar(id, max(x, self._get_bar(id)))

    def _check_min(self, id):
        return lambda x : self._set_bar(id, min(x, self._get_bar(id)))

    # constructor to create window
    def __init__(self, name):
        self._window_name = name
        cv2.namedWindow(self._window_name, cv2.WINDOW_AUTOSIZE)
        cv2.createTrackbar('Hue Min', self._window_name, 0, 180, self._check_max('Hue Max'))
        cv2.createTrackbar('Hue Max', self._window_name, 0, 180, self._check_min('Hue Min'))
        cv2.createTrackbar('Sat Min', self._window_name, 0, 255, self._check_max('Sat Max'))
        cv2.createTrackbar('Sat Max', self._window_name, 0, 255, self._check_min('Sat Min'))
        cv2.createTrackbar('Val Min', self._window_name, 0, 255, self._check_max('Val Max'))
        cv2.createTrackbar('Val Max', self._window_name, 0, 255, self._check_min('Val Min'))
        cv2.createTrackbar('Erode', self._window_name, 1, 50, nothing)
        cv2.createTrackbar('Dilate', self._window_name, 1, 50, nothing)
        cv2.createTrackbar('Cascades', self._window_name, 0, 1, nothing)
        self._set_bar('Hue Min', 000)
        self._set_bar('Hue Max', 180)
        self._set_bar('Sat Min', 000)
        self._set_bar('Sat Max', 255)
        self._set_bar('Val Min', 000)
        self._set_bar('Val Max', 255)
        self._set_bar('Erode', 1)
        self._set_bar('Dilate', 1)
        self._set_bar('Cascades', 0)
    
    def get_erode_size(self):
        return self._get_bar('Erode')

    def get_dilate_size(self):
        return self._get_bar('Dilate')

    def get_cascades(self):
        return self._get_bar('Cascades') > 0.5

    def min_thresholds(self):
        return (self._get_bar('Hue Min'), self._get_bar('Sat Min'), self._get_bar('Val Min'))
        
    def max_thresholds(self):
        return (self._get_bar('Hue Max'), self._get_bar('Sat Max'), self._get_bar('Val Max'))

    def imshow(self, img):
        cv2.imshow(self._window_name, img)

    def is_open(self):
        return cv2.getWindowProperty(self._window_name, 0) >= 0
