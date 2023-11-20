import time

from DinoGame import DinoController
import keyboard

game_controller = DinoController()
while True:
    if keyboard.is_pressed('tab'):
        time.sleep(1)
        game_controller.toggle_game_step()

    if game_controller.is_game_step:
        game_controller.play_game_step()

    else:
        game_controller.find_dino()
