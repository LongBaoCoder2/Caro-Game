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
import name
import game
import pygame
from lib.options import Options
from lib.music_player import MusicPlayer

class Main():
    # Khởi tạo
    def __init__(self):          
        # setting
        self.setting = json.load(open('data/setting.json'))
        self.SCREEN_WIDTH  = self.setting['screen']['width']
        self.SCREEN_HEIGHT = self.setting['screen']['height']
        # Khởi tạo option settings (Kích thước và toàn màn hình)
        self.options = Options(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.screen = pygame.display.set_mode(self.options.resolution)
        # self.MenuScreen = menu.Menu(self.screen)
        # NameScreen = name.Name(self.options.resolution[0], self.options.resolution[1], self.screen, "PvP")
        pygame.init()
        
        self.MenuScreen = None
        self.NameScreenPvP = None
        self.NameScreenAI = None
        self.GameScreen = None
        self.mode = "menu"
        self.music_player=MusicPlayer()
        # Khởi tạo các cửa sổ
        # Khởi tạo Menu
        # self.MenuScreen = menu.Menu(self.screen)
        # self.NameScreenPvP = name.Name(self.screen, "PvP")
        # self.NameScreenAI = None
        # self.GameScreen = game.
        
    def run(self):
        self.music_player.menu_play()
        while self.mode != "end":
            if self.mode == "menu":
                self.MenuScreen = menu.Menu(self.screen, self.music_player)
                self.mode = self.MenuScreen.run()
            elif self.mode == "PvP":
                self.NameScreenPvP = name.Name(self.screen, "PvP")
                self.mode = self.NameScreenPvP.run()
            elif self.mode == "AI":
                pass 
            elif self.mode == "new_game":
                self.GameScreen = game.Game(self.screen, self.music_player)
                self.music_player.menu_pause()
                self.music_player.ingame_sound_play()
                self.GameScreen.new_game()
                self.mode = self.GameScreen.run()
            elif self.mode == "continue_game":
                self.music_player.menu_pause()
                self.music_player.ingame_sound_play()
                self.GameScreen = game.Game(self.screen, self.music_player)
                # self.GameScreen.new_game()
                self.mode = self.GameScreen.run()

if __name__ == "__main__":
    main = Main()
    
    main.run()
    
    pygame.quit()
            
    # MusicGame.play('res/musicgame/musicgame1.mp3')
    # Chạy màn hình game
    

