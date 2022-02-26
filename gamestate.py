import cv2 as cv
from threading import Thread, Lock
from time import sleep, time
from detection import Detection

class GameState:
    
    # Threading properties
    stopped = True
    lock = Lock()

    # UI Locations
    buy_xp_img = None
    buy_xp_button_loc = None

    roll_button_img = None
    roll_button_lock = None


    lvl_loc = None
    stage_loc = None
    
    # Game Info
    screenshot = None
    gold_amount = 0
    streak = 0
    current_stage = (1,1)
    current_health = 100

    def __init__(self):
        self.buy_xp_img = cv.imread('img/buy-xp.jpg')
        self.buy_xp_button_loc = Detection.find_object(self.buy_xp_img, )

        self.roll_button_img_path = cv.imread('img/roll.jpg')

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()