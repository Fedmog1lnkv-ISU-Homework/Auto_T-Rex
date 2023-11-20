import time
import cv2
import keyboard
import numpy as np
from DinoGame.DinoCapturer import DinoCapturer


class DinoController:
    def __init__(self):
        self.dino_capturer = DinoCapturer()
        self.start_time = time.time()
        self.is_game_step = False
        self.crouch_delay = 0.27

    def calculate_offset(self):
        current_time = time.time()
        score = (current_time - self.start_time) * 10

        if score < 1000:
            offset = int((score // 100) * 8)
        else:
            offset = int(min((score // 100) * 15, 190))

        return offset, score

    def analyze_bottom_obstacle(self, offset, score):
        print("Offset:", offset, "Score:", score)
        bottom_obstacles_image = self.dino_capturer.find_bottom_obstacle(horizontal_offset=offset)

        if np.any(bottom_obstacles_image < 150):
            self.perform_jump()

    def perform_jump(self):
        keyboard.release('down')
        keyboard.press('space')
        time.sleep(self.crouch_delay)
        keyboard.release('space')
        keyboard.press('down')
        time.sleep(0.15)

    def play_game_step(self):
        offset, score = self.calculate_offset()
        self.analyze_bottom_obstacle(offset, score)

    def find_dino(self):
        self.dino_capturer.find_dino_on_screen()

    def toggle_game_step(self):
        self.is_game_step = not self.is_game_step
        time.sleep(0.5)
        if self.is_game_step:
            self.start_time = time.time()
