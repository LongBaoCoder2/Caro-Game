import pygame, json, game
import menu, winlose

# setting
setting = json.load(open('data/setting.json'))
SCREEN_WIDTH  = setting['screen']['width']
SCREEN_HEIGHT = setting['screen']['height']

if __name__ == "__main__":
    app = menu.Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
    app.run()
