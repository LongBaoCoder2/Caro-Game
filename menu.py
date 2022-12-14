import pygame, json
from lib import button, color

setting = json.load(open('data/setting.json'))
SCREEN_WIDTH  = setting['screen']['width']
SCREEN_HEIGHT = setting['screen']['height']

class Menu:
    
    # khởi tạo
    def __init__(self):
        self.img_one_player = [pygame.image.load('res/images/menu/one_player_' + str(i) + '.png') for i in range(2)]
        self.img_two_player = [pygame.image.load('res/images/menu/two_player_' + str(i) + '.png') for i in range(2)]
        self.btn_one_player = button.Button(self.img_one_player[0], 60, 500, 50, 50, 100, 100)
        self.btn_two_player = button.Button(self.img_two_player[0], SCREEN_WIDTH - self.img_one_player[0].get_width() - 60, 500, 50, 50, 100, 100)
        self.clock = pygame.time.Clock()

    # vòng lặp
    def loop_on(self, screen):

        # tô screen bằng màu background
        screen.fill(color.BACKGROUND)

        # thay đổi hình ảnh của button tuỳ theo hovered
        self.btn_one_player.update_image(self.img_one_player[1] if self.btn_one_player.is_hovered() else self.img_one_player[0])
        self.btn_two_player.update_image(self.img_two_player[1] if self.btn_two_player.is_hovered() else self.img_two_player[0])
        
        # vẽ button là screen
        self.btn_one_player.draw_on(screen)
        self.btn_two_player.draw_on(screen)

        # duyệt qua các event
        for event in pygame.event.get():
            # nếu người dùng bấm thoát
            if event.type == pygame.QUIT:
                return 0
        
        # cập nhật display
        pygame.display.update()

        # delay 120ms
        self.clock.tick(120)

        # nếu người chơi bấm chế độ 1 người
        if self.btn_one_player.is_clicked():
            return 1

        # nếu người chơi bấm chế độ 2 người
        if self.btn_two_player.is_clicked():
            return 2
        
        # nếu không có sự kiện gì thì trả về -1
        return -1
