from window import ThresholdWindow

import numpy as np
import cv2 

# Open up your webcam to read from
webcam = cv2.VideoCapture(0)

# make sliders for thresholds
display = ThresholdWindow("OpenCV Example")

# loop over and over again
while display.is_open():
    # read frame from webcam
    ret, frame = webcam.read()

    # convert to HSV then to Binary
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    binary_frame = cv2.inRange(hsv_frame, display.min_thresholds(), display.max_thresholds())
    
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

    # display images
    combined_frame = cv2.hconcat([frame,binary_frame])
    display.imshow(combined_frame)
    
    # quit if the q key is pressed
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# webcam release lets other programs use the webcam
webcam.release()

# destroy all windows makes sure that cv2 is really closed
cv2.destroyAllWindows()