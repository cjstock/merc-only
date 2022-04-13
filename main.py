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
from enum import Enum
from os import stat
from time import sleep, time
import cv2 as cv
import numpy as np
import pyautogui

from vision import Vision
from windowcapture import WindowCapture
from detection import Detection, Detector


class State(Enum):
    STOPPED = 1,
    INITIALIZING = 2,
    WAITING = 3,
    ROLLING = 4,
    DONE = 5

def main():
    print('Starting...')
    wincap = WindowCapture('League of Legends (TM) Client')
    print('Found Window')
    detection = Detection()
    print('Setup Detection')
    vision = Vision()

    DEBUG = True


    wincap.start()
    print('Started capturing')
    start_time = time()

    state = State.INITIALIZING
    detection.action(targets=['round-12'], action='start')
    detection.action(targets=['round-12'], action='update', args=wincap.screenshot)
    detection.action(targets=['round-12'], action='run')

    while(True):
        print(state.name)

        if state == State.INITIALIZING:
            detection.action(targets=['round-12'], action='update', args=wincap.screenshot)
            p = detection.detectors['round-12'].points
            if p:
                pyautogui.moveTo(p)
                state = State.WAITING
                sleep(5)

        if state == State.WAITING:
            if time() - start_time >= 15:
                continue
        
        if state == State.DONE:
            detection.bulk_action(action='stop')
            wincap.stop()
            cv.destroyAllWindows()
            break

        #detection.bulk_action(action='update', arg=wincap.screenshot)
        #detection.bulk_action(action='get_click_points')


        if DEBUG:
            debug_img = None
            for d in detection.detectors.values():
                debug_img = vision.draw_rectangles(wincap.screenshot, d.rectangles)
            cv.imshow('Matches', debug_img)


    print('Done.')
main()