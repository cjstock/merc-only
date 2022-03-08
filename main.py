'''
The bot performs the following actions based on the gamestate:
Wait 20 seconds
0. Find locations of key UI elements
    - level, gold, stage, reroll button, xp button, augments, etc
1. Find mercs phase
    0. Search for early Merc units
    1. Select Merc-centric augments
    2. Stay strong
2. Loss streak
    0. Collect mercs but not two star
    1. Collect champions that share Merc traits
    2. Priority- econ
    3. Stop at 40hp
    4. Hold items
3. Try to Cash
    0. Two star all champions
    1. Slam items
    2. Level up
'''
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