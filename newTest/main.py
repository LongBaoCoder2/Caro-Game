import pygame, json, game
import menu

# setting
setting = json.load(open('data/setting.json'))
SCREEN_WIDTH  = setting['screen']['width']
SCREEN_HEIGHT = setting['screen']['height']

if __name__ == "__main__":
    # Khởi tạo Menu
    app = menu.Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
    # Chạy màn hình game
    app.run()
