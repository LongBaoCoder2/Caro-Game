import sys
import os

if sys.platform.startswith("linux"):  # could be "linux", "linux2", "linux3", ...
    # linux
    pass
elif sys.platform == "darwin":
    # MAC OS X
    pass
elif os.name == "nt":
    # https://stackoverflow.com/a/44341598
    # this prevent pygame from scretching its window UI
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
    # Windows, Cygwin, etc. (either 32-bit or 64-bit)

import json
import menu

# setting
setting = json.load(open('data/setting.json'))
SCREEN_WIDTH  = setting['screen']['width']
SCREEN_HEIGHT = setting['screen']['height']

if __name__ == "__main__":
    # Khởi tạo Menu
    app = menu.Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # MusicGame.play('res/musicgame/musicgame1.mp3')
    # Chạy màn hình game
    app.run()

