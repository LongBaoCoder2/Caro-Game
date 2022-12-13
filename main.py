import pygame, json, menu, game

# setting
setting = json.load(open('data/setting.json'))
SCREEN_WIDTH  = setting['screen']['width']
SCREEN_HEIGHT = setting['screen']['height']

if __name__ == "__main__":
    
    # khởi tạo pygame
    pygame.init()

    # tạo screen bằng pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu_scene = menu.Menu()
    game_scene = game.Game()

    # vòng lặp chính của chương trình
    (running, playing) = (True, False)
    while (running):        

        # nếu không đang chơi thì hiện game menu và lấy sự kiện trả về
        if playing == False:
            pygame.display.set_caption("menu scene")
            menu_ret = menu_scene.loop_on(screen)

            # nếu menu trả về chế độ 2 người (chơi mới)
            if menu_ret == 1:
                playing = True
                game_scene.new_game(screen)
            
            # nếu menu trả về chế độ 1 người (chơi tiếp)
            if menu_ret == 2:
                playing = True
                game_scene.continue_game(screen)

        # nếu đang chơi
        else:
            # vòng lặp cho game
            pygame.display.set_caption("game scene")
            game_scene.loop_on(screen)
    
        # print(pygame.mouse.get_pos())
