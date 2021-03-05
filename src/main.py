from window import ThresholdWindow

import os
import numpy as np
import cv2 
from random import random

# open up benchmark image
benchmark = cv2.imread("./benchmark.png")
hsv_benchmark = cv2.cvtColor(benchmark, cv2.COLOR_BGR2HSV)

# open up your webcam to read from
webcam = cv2.VideoCapture(0)

# all of the things to play
DIRECTORY = './haarcascades/'
cascades = []
for filename in os.listdir(DIRECTORY):
    file = DIRECTORY + filename
    try:
        cascade = [ ((random() * 255, random() * 255, random() * 255), cv2.CascadeClassifier(file)) ]
        cascades += cascade
        print(file + " is set to color: " + str(cascade[0]))
    except Exception as e:
        print(file + " failed to open")
        pass

# make sliders for thresholds
display = ThresholdWindow("OpenCV Example")

# loop over and over again
while display.is_open():
    # read frame from webcam
    ret, frame = webcam.read()

    # convert to HSV then to Binary
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    binary_frame = cv2.inRange(hsv_frame, display.min_thresholds(), display.max_thresholds())

    # cascades
    if(display.get_cascades()):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        for color, cascade in cascades:
            objects = cascade.detectMultiScale(gray_frame, 1.3, 5)
            for (x,y,w,h) in objects:
                frame = cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)

    # erode and dilate the images
    erode_level = display.get_erode_size()
    dilate_level = display.get_dilate_size()
    erode_kernel = np.ones((erode_level, erode_level), np.uint8)
    dilate_kernel = np.ones((dilate_level, dilate_level), np.uint8)
    binary_frame = cv2.erode(binary_frame, erode_kernel)
    binary_frame = cv2.dilate(binary_frame, dilate_kernel)

    # use opencv to find contours
    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # after finding contours, make binary image have color
    binary_frame = cv2.cvtColor(binary_frame, cv2.COLOR_GRAY2BGR)

    # look for contours
    if len(contours) != 0:
        # loop through all contours and get the biggest one
        largest = contours[0]
        for contour in contours:
            if cv2.contourArea(largest) < cv2.contourArea(contour):
                largest = contour 

        cv2.drawContours(frame, [largest], -1, 255, 3)
        cv2.drawContours(binary_frame, [largest], -1, 255, 3)

    # threshold benchmark image
    binary_benchmark = cv2.inRange(hsv_benchmark, display.min_thresholds(), display.max_thresholds())
    cv2.imshow("Benchmark Test", cv2.bitwise_and(benchmark, benchmark, mask=binary_benchmark))

    # display images
    display.imshow(cv2.hconcat([frame, binary_frame]))
    
    # quit if the q key is pressed
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# webcam release lets other programs use the webcam
webcam.release()

# destroy all windows makes sure that cv2 is really closed
cv2.destroyAllWindows()