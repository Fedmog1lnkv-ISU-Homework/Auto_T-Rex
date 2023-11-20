import cv2
import numpy as np
from mss import mss


class DinoCapturer:
    def __init__(self, dino_path='files/dino.png'):
        self.capturer = mss()
        self.monitor = self.capturer.monitors[0]

        self.dino_image = cv2.imread(dino_path, cv2.IMREAD_GRAYSCALE)
        self.dino_image = cv2.Canny(self.dino_image, 100, 200)
        
        self.dino_location = None

        self.dino_width = 0
        self.dino_height = 0

    def find_bottom_obstacle(self, horizontal_offset):
        top_offset = 5
        monitor = {
            "top": self.dino_location[1] + top_offset,
            "left": self.dino_location[0] + self.dino_width,
            "width": self.dino_width + horizontal_offset,
            "height": 25
        }

        screenshot = np.array(self.capturer.grab(monitor))
        return screenshot

    def find_dino_on_screen(self):
        screenshot = self.capturer.grab(self.monitor)
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        screenshot = cv2.Canny(screenshot, 100, 200)

        w, h = self.dino_image.shape
        result = cv2.matchTemplate(screenshot, self.dino_image, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        self.dino_location = max_loc
        self.dino_width, self.dino_height = w, h
        return max_loc, (max_loc[0] + w, max_loc[1] + h)
