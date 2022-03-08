import cv2 as cv
from threading import Lock, Thread
from os import listdir

from numpy import array, rec


class Detection:
    
    needles = []
    detectors = {}
    
    def __init__(self):
        
        # get names of needles stripped of .jpg
        self.needles = [x[:-4] for x in listdir('needles')]

        # add all needles to detector
        for needle in self.needles:
            self.add(needle)


    def bulk_action(self, targets=None, action='', arg=[]):
        '''
        Description: Calls an action on a set of detectors defined by targets.
        targets (list of needle names)
        action (string)
        '''
        if not targets:
            targets = self.needles
        for t in targets:
            d = self.detectors.get(t)
            if len(arg) != 0:
                getattr(d, action)(arg)
            else:
                getattr(d, action)()

    def add(self, needle):
        self.detectors[needle] = Detector(needle)


class Detector:
    '''
    Responsible for detecting a given game object.
    '''
    screenshot = None
    needle_img = None
    needle_w = 0
    needle_h = 0

    # threading properties
    stopped = True
    lock = None

    rectangles = []
    points = []

    def __init__(self, needle_name):
        self.lock = Lock()
        self.needle_img = cv.imread('needles/'+ needle_name + '.jpg')
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]


    def find_object(self, haystack_img, threshold=0.8, use_method='minMaxLoc'):
        rectangles = []

        result = cv.matchTemplate(haystack_img, self.needle_img, method=cv.TM_CCOEFF_NORMED)

        if use_method == 'minMaxLoc':
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if max_val >= threshold:
                top_left = max_loc
                rectangles.append((*top_left, self.needle_w, self.needle_h))
        
        return rectangles

    def get_click_points(self):
        points = []

        # Loop over all the rectangles
        for (x, y, w, h) in self.rectangles:
            # Determine the center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # Save the points
            points.append((center_x, center_y))

        return points

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if not self.screenshot is None:
                rectangles = self.find_object(self.screenshot)

                self.lock.acquire()
                self.rectangles = rectangles
                self.points = self.get_click_points()
                self.lock.release()