import numpy as np
import win32gui
import cv2 as cv
import pyautogui
from threading import Thread, Lock


class WindowCapture:

    # threading properties
    stopped = True
    lock = None
    screenshot = None


    # properties
    hwnd = None
    w = 0
    h = 0
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name):
        self.lock = Lock()

        # wait for window to appear
        while not self.hwnd:
            self.hwnd = win32gui.FindWindow(None, window_name)

        win32gui.SetForegroundWindow(self.hwnd)

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y
        

    def get_screenshot(self):
        x, y, x1, y1 = win32gui.GetClientRect(self.hwnd)
        x, y = win32gui.ClientToScreen(self.hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(self.hwnd, (x1 - x, y1 - y))
        img = pyautogui.screenshot(region=(x, y, x1, y1))
        img = np.array(img)
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        return img

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            temp_ss = self.get_screenshot()

            self.lock.acquire()
            self.screenshot = temp_ss
            self.lock.release()