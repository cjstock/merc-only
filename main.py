from time import time

import cv2 as cv
import numpy as np
import pyautogui

from vision import Vision
from windowcapture import WindowCapture
from detection import Detection, Detector

def main():
    # initialize the WindowCapture class
    wincap = WindowCapture('League of Legends (TM) Client')
    detection = Detection()
    vision = Vision()

    DEBUG = True


    wincap.start()
    detection.bulk_action(action='start')

    while(True):

        if wincap.screenshot is None:
            continue

        detection.bulk_action(action='update', arg=wincap.screenshot)
        detection.bulk_action(action='get_click_points')


        if DEBUG:
            debug_img = None
            for d in detection.detectors.values():
                debug_img = vision.draw_rectangles(wincap.screenshot, d.rectangles)
            cv.imshow('Matches', debug_img)

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            detection.bulk_action(action='stop')
            wincap.stop()
            cv.destroyAllWindows()
            break

    print('Done.')
main()