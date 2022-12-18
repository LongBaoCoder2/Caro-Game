import pygame, json, game
import menu

# setting
setting = json.load(open('data/setting.json'))
SCREEN_WIDTH  = setting['screen']['width']
SCREEN_HEIGHT = setting['screen']['height']

clock = pygame.time.Clock()

if __name__ == "__main__":
    app = menu.Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
    app.run()
