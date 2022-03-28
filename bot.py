import cv2 as cv
from time import sleep, time
from threading import Thread, Lock


class TFTBot:

    lock = None

    state = None
    timestamp = None

    screenshot = None
    
    def __init__(self):
        self.lock = Lock()

        self.timestamp = time()

    def roll(self):
        pass

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()