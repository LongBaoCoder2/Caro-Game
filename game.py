import pygame, json
from lib import color, save_manager, win_checker, bot

setting = json.load(open('data/setting.json'))
# screen
SCREEN_WIDTH  = setting['screen']['width']
SCREEN_HEIGHT = setting['screen']['height']
# grid
# NUM_OF_LINES  = setting['grid']['num_of_lines']
SIZE_X    = setting['grid']['size_x']
SIZE_Y    = setting['grid']['size_y']
THICKNESS = setting['grid']['thickness']
# GRID_COLOR    = [setting['grid']['color_0'], setting['grid']['color_1']]
# theme
THEME = setting['theme']

class Game:

    # khởi tạo
    def __init__(self):
        # ----- img -----
        self.img_grid  =  pygame.image.load('res/images/' + THEME + '/grid.png')
        self.img_piece = [pygame.image.load('res/images/' + THEME + '/piece_' + str(i) + '.png') for i in range(2)]

        # ----- grid -----
        # self.grid_width  = (SCREEN_WIDTH  - THICKNESS * NUM_OF_LINES) // (NUM_OF_LINES - 1) + THICKNESS
        # self.grid_height = (SCREEN_HEIGHT - THICKNESS * NUM_OF_LINES) // (NUM_OF_LINES - 1) + THICKNESS
        self.grid_width   = self.img_grid.get_width() // 2
        self.grid_height  = self.img_grid.get_width() // 2
        self.grid_start_x = 30
        self.grid_start_y = 30 + 128
        self.grid_end_x = self.grid_start_x + self.grid_width  * SIZE_X
        self.grid_end_y = self.grid_start_y + self.grid_height * SIZE_Y

        # ----- img -----
        self.save_manager = save_manager.SaveManager('game_data.json', 'data')
        self.game_data    = self.save_manager.load()

        # ----- win -----
        self.win_checker = win_checker.WinChecker()

        # ----- clock -----
        self.clock = pygame.time.Clock()

        # ----- bot -----
        self.bot = bot.Bot()

    # khởi tạo game mới
    def new_game(self, screen):
        self.draw_grid_on(screen)
        self.game_data = self.save_manager.refresh()

    # tiếp tục game từ save
    def continue_game(self, screen):
        self.draw_grid_on(screen)
        for row in range(SIZE_X):
            for column in range(SIZE_Y):
                piece_data = self.game_data['Board'][row][column]
                # nếu không chứa cờ thì bỏ qua
                if piece_data == -1:
                    continue
                # lấy hình ảnh cờ tương ứng theo data
                cur_piece = self.img_piece[piece_data]
                # tính vị trí của cờ để vẽ
                pos_piece = (self.grid_start_x + self.grid_width * row, self.grid_start_y + self.grid_height * column)
                # vẽ cờ lên màn hình
                screen.blit(cur_piece, pos_piece)

    # vẽ lưỡi lên một surface
    def draw_grid_on(self, screen):

        # tô screen bằng màu background
        screen.fill(color.BACKGROUND)

        for i in range(self.grid_start_x, SCREEN_WIDTH - self.grid_width * 2, self.grid_width * 2):
            for j in range(self.grid_start_y, SCREEN_HEIGHT - self.grid_height * 2, self.grid_height * 2):
                screen.blit(self.img_grid, (i, j))

        # # vẽ các ô màu xen kẽ
        # for i in range(0, SCREEN_WIDTH, self.grid_width):
        #     for j in range(0, SCREEN_HEIGHT, self.grid_height):
        #         pygame.draw.rect(screen, GRID_COLOR[(i + j) % 2], (i, j, self.grid_width, self.grid_height))
        
        # # vẽ các đường dọc
        # for i in range(self.grid_width, SCREEN_WIDTH - self.grid_width, self.grid_width):
        #     pygame.draw.line(screen, color.BLACK, (i + THICKNESS // 2, 40), (i + THICKNESS // 2, SCREEN_HEIGHT - 40), THICKNESS)

        # # vẽ cách đường ngang
        # for i in range(self.grid_height, SCREEN_HEIGHT - self.grid_height, self.grid_height):
        #     pygame.draw.line(screen, color.BLACK, (40, i + THICKNESS // 2), (SCREEN_WIDTH - 40, i + THICKNESS // 2), THICKNESS)

    def draw_piece_on(self, screen, board_x, board_y, cur_piece):
        # đưa về dạng tâm của bàn cờ
        (center_x, center_y) = (board_x * self.grid_width + (self.grid_width + THICKNESS) // 2, board_y * self.grid_width + (self.grid_width + THICKNESS) // 2)

        # đưa về dạng góc trái trên của cờ trong bàn cờ
        display_pos = (center_x + self.grid_start_x - cur_piece.get_width() / 2, center_y + self.grid_start_y - cur_piece.get_height() / 2)
        
        # vẽ cờ lên màn hình
        screen.blit(cur_piece, display_pos)

    # vòng lặp
    def loop_on(self, screen):

        # duyệt qua các event
        for event in pygame.event.get():

            # nếu người chơi bấm chuột trái
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # lấy hình ảnh của cờ theo turn
                    cur_piece = self.img_piece[self.game_data['Turn']]

                    # lấy vị trí của chuột khi click
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()

                    # nếu vị trí click nằm ngoài bàn cờ thì bỏ qua
                    if mouse_x < self.grid_start_x or mouse_x > self.grid_end_x or mouse_y < self.grid_start_y or mouse_y > self.grid_end_y:
                        continue

                    # đưa về vị trí trong bảng
                    (board_x, board_y) = ((mouse_x - self.grid_start_x) // self.grid_width, (mouse_y - self.grid_start_y) // self.grid_width)

                    # nếu bảng đã chứa cờ thì bỏ qua
                    if self.game_data['Board'][board_x][board_y] != -1:
                        continue

                    # vẽ cờ lên màn hình
                    self.draw_piece_on(screen, board_x, board_y, cur_piece)

                    # cập nhật display
                    pygame.display.update()

                    # lưu lại giá trị trong bảng
                    self.game_data['Board'][board_x][board_y] = self.game_data['Turn']
                    
                    # kiểm tra đã thắng chưa
                    if self.win_checker.check_win(self.game_data['Board'], self.game_data['Turn'], board_x, board_y):
                        print('NGUOI THANG!')
                        
                    # Thay đổi Turn ở cuối mỗi lượt
                    self.game_data['Turn'] = 1 - self.game_data['Turn']

                    # Comment these lines to enable PvP mode
                    """
                    # Mah Cute Bot
                    best_move = self.bot.find_best_move(self.game_data['Board'])
                    self.draw_piece_on(screen, best_move[0], best_move[1], self.img_piece[1])
                    self.game_data['Board'][best_move[0]][best_move[1]] = 1
                    if self.win_checker.check_win(self.game_data['Board'], self.game_data['Turn'], board_x, board_y):
                        print('BOT THANG!')
                    self.game_data['Turn'] = 1 - self.game_data['Turn']
                    """
                    
            
            # nếu người dùng bấm thoát
            if event.type == pygame.QUIT:
                # save game trước khi thoát
                self.save_manager.save(self.game_data)
                return 0

        # cập nhật display
        pygame.display.update()
        
        # delay 120ms
        self.clock.tick(120)
        
        # nếu không có sự kiện gì thì trả về -1
        return -1
