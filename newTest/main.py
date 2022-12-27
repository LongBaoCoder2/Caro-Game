# https://stackoverflow.com/a/44341598
# this prevent pygame from scretching its window UI
# import ctypes
# ctypes.windll.user32.SetProcessDPIAware()

import pygame, json, game
import menu
from lib.music_game import MusicGame

# setting
setting = json.load(open('data/setting.json'))
SCREEN_WIDTH  = setting['screen']['width']
SCREEN_HEIGHT = setting['screen']['height']

if __name__ == "__main__":
    # Khởi tạo Menu
    app = menu.Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    MusicGame.play('res/musicgame/musicgame1.mp3')
    # Chạy màn hình game
    app.run()

