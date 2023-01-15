import pygame, json, sys, pygame_gui
#from lib.play_sound import PlaySound
from lib import color, save_manager, win_checker
from lib import text_switcher, cursor_trail, bot, pause
from lib import winlose, options
import menu
from lib.exit_window import *
from lib.music_player import MusicPlayer


class Game:

    # khởi tạo
    def __init__(self, screen, music_player):
        
        self.music_player=music_player
        # self.music_player.bgsound_play()
        # self.music_player.menu_pause()

        pygame.display.set_caption('GAME')
        
        theme_color = json.load(open('themes/theme.json'))
        self.setting = json.load(open('data/setting.json'))
        # Khởi tạo Screen
        self.screen = screen
        self.SCREEN_WIDTH  = self.setting['screen']['width']
        self.SCREEN_HEIGHT = self.setting['screen']['height']
        # grid
        # NUM_OF_LINES  = setting['grid']['num_of_lines']
        self.SIZE_X        = min(self.setting['grid']['size_x'], 100)
        self.SIZE_Y        = min(self.setting['grid']['size_y'], 100)
        self.THICKNESS     = self.setting['grid']['thickness']
        # GRID_COLOR    = ["#5D5FEF", "#843CE0"]
        # GRID_COLOR = [setting['grid']['color_0'], setting['grid']['color_1']]
        
        # Tạo tùy chọn cho màn hình
        self.options = options.Options(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        # Tạo background (sẽ setup sau)
        self.background_surface = None
        self.BACKGROUND_COLOR = "#501be8"
        
        self.LINE_COLOR       = color.BLACK
        # theme
        self.THEME = self.setting['theme']

        # lấy dữ liệu gamemode từ setting.json
        self.gamemode = self.setting["gamemode"]

        # pygame clock
        self.clock = pygame.time.Clock()

        # ảnh lưới và cờ
        self.img_grid  = pygame.transform.scale(pygame.image.load('res/images/' + self.THEME + '/grid2.png'), (64, 64))
        self.img_piece = [pygame.transform.scale(pygame.image.load('res/images/' + self.THEME + '/piece_' + str(i) + '.png'), (32, 32)) for i in range(2)]

        # một số thông tin về lưới
        # self.grid_width  = 32
        # self.grid_height = 32
        # self.grid_width  = (SCREEN_WIDTH  - THICKNESS * NUM_OF_LINES) // (NUM_OF_LINES - 1) + THICKNESS
        # self.grid_height = (SCREEN_HEIGHT - THICKNESS * NUM_OF_LINES) // (NUM_OF_LINES - 1) + THICKNESS
        self.grid_width   = self.img_grid.get_width() // 2
        self.grid_height  = self.img_grid.get_width() // 2
        self.grid_start_x = (self.SCREEN_HEIGHT - self.grid_height * self.SIZE_Y) * 1 // 4
        self.grid_start_y = (self.SCREEN_HEIGHT - self.grid_height * self.SIZE_Y) * 3 // 8
        self.grid_end_x   = self.grid_start_x + self.grid_width  * self.SIZE_X
        self.grid_end_y   = self.grid_start_y + self.grid_height * self.SIZE_Y

        # Tạo một manager UI (Quản lý Giao diện màn hình)
        # Tham số truyền vào sẽ là kích thước màn hình và package
        # Hãy xem manager như là một người quản lý màn hình:
        # Với công việc là set up background và vẽ button quản lý các hiệu ứng v.v
        self.manager = pygame_gui.UIManager(self.options.resolution, 
                                            pygame_gui.PackageResource(package='themes',
                                                            resource='theme.json'))

        self.btn_size = (int(self.options.resolution[0] * 0.4), int(self.options.resolution[1] * 0.1))
        self.text_entry_size = (int(self.options.resolution[0] * 0.6) , int(self.options.resolution[1] * 0.1))
        self.label_size = (int(self.options.resolution[0] * 0.6), int(self.options.resolution[1] * 0.25))

        # Screen Win Lose
        # --- Đưa window vào center
        window_RECT = pygame.Rect((0,0), (self.SCREEN_WIDTH * 5 // 8, self.SCREEN_HEIGHT * 5 // 8))
        window_RECT.center = (self.SCREEN_WIDTH / 2 , self.SCREEN_HEIGHT / 2)
        
        # Khởi tạo
        # chiều rộng (ngang) cửa sổ settings, quit
        sub_window_width = self.options.resolution[0] * 5 // 8
        # chiều cao (dọc) cửa sổ settings, quit
        sub_window_height = self.options.resolution[1] * 5 // 8 
        self.win_lose_screen = winlose.WinLoseWindow(window_RECT, self.manager, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, "")
        #self.music_player.bgsound_pause()
        self.pause_screen = pause.PauseWindow(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2 - 50),
                                                        int(self.options.resolution[1] / 2) - 125), 
                                                        (sub_window_width * 3 // 4, sub_window_height * 3 // 5)),
                                                        self.manager, self.options.resolution[0], self.options.resolution[1])
        self.exit_screen = ExitWindow(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2 - 50),
                                                        int(self.options.resolution[1] / 2) - 125), 
                                                        (sub_window_width * 3 // 4, sub_window_height * 3 // 5)),
                                                        self.manager, self.options.resolution[0], self.options.resolution[1])
        
        # Ban đầu ẩn màn hình nhỏ đi
        self.win_lose_screen.hide()
        self.exit_screen.hide()
        self.pause_screen.hide()
        
        # Button điều hướng khi chiến thắng trò chơi
        # Này demo trước, sau tách ra thành một class riêng
        
        self.btn_play_again = pygame_gui.elements.UIButton(pygame.Rect((int(self.SCREEN_WIDTH * 0.65),
                                                        int(self.SCREEN_HEIGHT * 0.4)), 
                                                        tuple(i * 3 // 4 for i in self.btn_size)),
                                                        "Play Again",
                                                        self.manager,
                                                        object_id="#all_button")
        self.btn_menu = pygame_gui.elements.UIButton(pygame.Rect((int(self.SCREEN_WIDTH * 0.65),
                                                        int(self.SCREEN_HEIGHT * 0.5)), 
                                                        tuple(i * 3 // 4 for i in self.btn_size)),
                                                        "Menu",
                                                        self.manager,
                                                        object_id="#all_button")
        self.btn_quit = pygame_gui.elements.UIButton(pygame.Rect((int(self.SCREEN_WIDTH * 0.65),
                                                        int(self.SCREEN_HEIGHT * 0.6)), 
                                                        tuple(i * 3 // 4 for i in self.btn_size)),
                                                        "Quit",
                                                        self.manager,
                                                        object_id="#all_button")
        
        self.btn_pause = pygame_gui.elements.UIButton(pygame.Rect((int(self.SCREEN_WIDTH * 0.75),
                                                        int(10)), 
                                                        (self.btn_size[0] * 4 // 8, self.btn_size[1] * 3 // 4)),
                                                        "Pause",
                                                        self.manager,
                                                        object_id="#all_button")
        
        # Ẩn các button này đi
        self.btn_play_again.hide()
        self.btn_menu.hide()
        self.btn_quit.hide()

        # các thành phần điều khiển của game
        self.save_manager  = save_manager.SaveManager('game_data.json', 'data')
        self.game_data     = self.save_manager.load()
        self.win_checker   = win_checker.WinChecker()
        self.player_1      = self.game_data['PlayerName']['Player1']
        self.player_2      = self.game_data['PlayerName']['Player2']
        self.text_switcher = text_switcher.TextSwitcher(self.screen, self.BACKGROUND_COLOR, 
                                                        [self.player_1, self.player_2], self.game_data['Turn'])
        self.cursor_trail  = cursor_trail.CursorTrail()
        self.bot           = bot.Bot()

        # for bot
        self.end_game = False
        self.cnt_move = 0
        self.turn     = self.game_data['Turn']
        self.history  = list()
        self.max_his  = 10
        
        #biến vòng lặp game
        # self.running = True
        self.running_mode = "game"
        
        # Setup Background
        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.manager.get_theme().get_colour("dark_bg"))  # dark_bg nằm trong file theme.json
        
        # self.exit_screen_created = False
        # self.winlose_window_created = False
        # self.blocked = False

    # khởi tạo game mới
    def new_game(self):
        self.draw_grid_on()
        self.game_data = self.save_manager.refresh()

    # tiếp tục game từ save
    def continue_game(self):
        self.draw_grid_on()
        for row in range(self.SIZE_X):
            for column in range(self.SIZE_Y):
                piece_data = self.game_data['Board'][row][column]
                # nếu không chứa cờ thì bỏ qua
                if piece_data == -1:
                    continue
                # lấy hình ảnh cờ tương ứng theo data
                cur_piece = self.img_piece[piece_data]
                # tính vị trí của cờ để vẽ
                pos_piece = (self.grid_start_x + self.grid_width * row, self.grid_start_y + self.grid_height * column)
                # vẽ cờ lên màn hình
                self.screen.blit(cur_piece, pos_piece)

    # vẽ lưỡi lên một surface
    def draw_grid_on(self):

        # tô screen bằng màu background
        #self.screen.fill(self.BACKGROUND_COLOR)
        # for i in range(self.grid_start_x, SCREEN_WIDTH - self.grid_width * 2, self.grid_width * 2):
        #     for j in range(self.grid_start_y, SCREEN_HEIGHT - self.grid_height * 2, self.grid_height * 2):
        #         self.screen.blit(self.img_grid, (i, j))

        cur_y = self.grid_start_y
        for i in range(self.SIZE_Y // 2):
            cur_x = self.grid_start_x
            for j in range(self.SIZE_X // 2):
                self.screen.blit(self.img_grid, (cur_x, cur_y))
                cur_x += self.grid_height * 2
            if self.SIZE_X % 2 == 1:
                cur_x -= self.grid_height
                self.screen.blit(self.img_grid, (cur_x, cur_y))
            cur_y += self.grid_width * 2
        if self.SIZE_Y % 2 == 1:
            cur_y -= self.grid_width
            cur_x = self.grid_start_x
            for j in range(self.SIZE_X // 2):
                self.screen.blit(self.img_grid, (cur_x, cur_y))
                cur_x += self.grid_height * 2
            if self.SIZE_X % 2 == 1:
                cur_x -= self.grid_height
                self.screen.blit(self.img_grid, (cur_x, cur_y))

        delta = 10
        pygame.draw.rect(self.screen, self.LINE_COLOR, (self.grid_start_x - delta, self.grid_start_y - delta, self.grid_end_x - self.grid_start_x + delta * 2, self.grid_end_y - self.grid_start_y + delta * 2), 5, 10)

        # # vẽ các ô màu xen kẽ
        # for i in range(0, SCREEN_WIDTH, self.grid_width):
        #     for j in range(0, SCREEN_HEIGHT, self.grid_height):
        #         pygame.draw.rect(self.screen, GRID_COLOR[(i + j) % 2], (i, j, self.grid_width, self.grid_height))
        
        # # vẽ các đường dọc
        # for i in range(self.grid_width, SCREEN_WIDTH - self.grid_width, self.grid_width):
        #     pygame.draw.line(self.screen, color.BLACK, (i + THICKNESS // 2, 40), (i + THICKNESS // 2, SCREEN_HEIGHT - 40), THICKNESS)

        # # vẽ cách đường ngang
        # for i in range(self.grid_height, SCREEN_HEIGHT - self.grid_height, self.grid_height):
        #     pygame.draw.line(self.screen, color.BLACK, (40, i + THICKNESS // 2), (SCREEN_WIDTH - 40, i + THICKNESS // 2), THICKNESS)

    # vẽ cờ lên màn hình
    def draw_piece_on(self, board_x, board_y, cur_piece):
        # đưa về dạng tâm của bàn cờ
        (center_x, center_y) = (board_x * self.grid_width + (self.grid_width + self.THICKNESS) // 2, board_y * self.grid_width + (self.grid_width + self.THICKNESS) // 2)

        # đưa về dạng góc trái trên của cờ trong bàn cờ
        display_pos = (center_x + self.grid_start_x - cur_piece.get_width() / 2, center_y + self.grid_start_y - cur_piece.get_height() / 2)
        
        # vẽ cờ lên màn hình
        self.screen.blit(cur_piece, display_pos)

    def add_to_history(self, board_x, board_y):

        # thêm vị trí mới nhất của cờ vào list
        self.history.append((board_x, board_y))

        # nếu độ dài của list vượt quá giới hạn
        if len(self.history) > self.max_his:

            # xoá vị trí cũ nhất trong list
            del self.history[0]

    # process check win 
    def check_process(self, board_x, board_y) -> None:
        if self.win_checker.check_win(self.game_data['Board'], self.game_data['Turn'], board_x, board_y):
            # Save game trước khi làm việc khác
            #game_data = save_manager.SaveManager('game_data.json', 'data').refresh()
            self.game_data['PlayerName']['Player1'] = self.player_1
            self.game_data['PlayerName']['Player2'] = self.player_2
            self.end_game = True
            self.game_data["GameEnded"] = True
            #print(self.game_data)
            save_manager.SaveManager('game_data.json', 'data').save(self.game_data)
            win_player_name = self.player_1 if self.game_data['Turn'] == 1 else self.player_2
            self.win_lose_screen.set_name(win_player_name)
            
            self.win_lose_screen.show()
            self.btn_play_again.show()
            self.btn_menu.show()
            self.btn_quit.show()
            self.music_player.ingame_sound_pause()
            self.music_player.win_play()
            
            # self.win_lose_screen.run()       

    # vòng lặp
    def loop_on(self):
        # nếu đã đánh hết bàn cờ
        if self.SIZE_X * self.SIZE_Y == self.cnt_move:
            self.end_game = True

        # duyệt qua các event
        for event in pygame.event.get():
            
            # xử lý bot
            if self.gamemode == "Bot":
                if self.turn == 1:
                    # Comment these lines to enable PvP mode
                    if self.SIZE_X * self.SIZE_Y != self.cnt_move:
                        best_move = self.bot.find_best_move(self.game_data['Board'], self.history)
                        cur_piece = self.img_piece[self.game_data['Turn']]
                        self.draw_piece_on(best_move[0], best_move[1], cur_piece)
                        self.add_to_history(best_move[0], best_move[1])
                        self.game_data['Board'][best_move[0]][best_move[1]] = 1
                        self.cnt_move += 1
                        # check xem bot win hay thua
                        self.check_process(best_move[0], best_move[1])
                        
                        # if self.win_checker.check_win(self.game_data['Board'], 1, best_move[0], best_move[1]):
                        #     print('BOT WIN!')
                        #     self.end_game = True
                        self.game_data['Turn'] = 1 - self.game_data['Turn']
                        self.turn = 0
            
            
            # Quản lý và xử lý các sự kiện (như click, hover, ...)
            # Nếu thiếu dòng này thì pygame_gui sẽ không detect được việc mình đã nhấn nút hay chưa
            self.manager.process_events(event)
            
            quit_button_pressed = (event.type == pygame.QUIT)
            # if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            #     print(True)
            
            #print(self.exit_screen.visible)
            if quit_button_pressed or event.type == pygame_gui.UI_BUTTON_PRESSED:
                
                # print("Triggered")
                
                if quit_button_pressed or event.ui_element == self.btn_quit:
                    self.exit_screen.show()
                    
                elif event.ui_element == self.btn_pause:
                    self.pause_screen.show()
                
                elif event.ui_element == self.pause_screen.btn_Resume:
                    self.pause_screen.hide()
                
                #cửa sổ nào hiện sau thì cừa sổ đó đè lên cửa sổ  còn lại
                
                elif self.exit_screen.visible:
                    if event.ui_element == self.exit_screen.btn_Exit:
                        #print("Hello")
                        #print(self.game_data)
                        self.save_manager.save(self.game_data)
                        self.running_mode = "end"
                        break
                            
                    if event.ui_element == self.exit_screen.btn_continue:
                        self.exit_screen.hide()
                
                
                elif event.ui_element == self.win_lose_screen.btn_back:
                    self.win_lose_screen.hide()
                
                
                # Điều hướng sau khi chơi
                # elif 
                elif event.ui_element == self.btn_play_again:
                    self.game_data = save_manager.SaveManager('game_data.json', 'data').refresh()
                    self.game_data['PlayerName']['Player1'] = self.player_1
                    self.game_data['PlayerName']['Player2'] = self.player_2
                    save_manager.SaveManager('game_data.json', 'data').save(self.game_data)
                    self.__init__(self.screen, self.music_player)
                    # self.__init__(self.screen)
                    self.music_player.ingame_sound_play()
                    self.new_game()
                    self.run()
            
                elif event.ui_element == self.btn_menu or event.ui_element == self.pause_screen.btn_menu:
                    if event.ui_element == self.pause_screen.btn_menu:
                        self.game_data["Turn"] = self.turn
                        self.save_manager.save(self.game_data)
                    self.running_mode = "menu"
                    self.music_player.ingame_sound_pause()
                    self.music_player.menu_play()
                    break
                    # menu.Menu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT).run()
                
                #self.exit_screen_created = quit_button_pressed or btn_quit_clicked
                #print(self.exit_screen_created)
            
            # nếu người chơi bấm chuột trái
            elif (not self.exit_screen.visible 
                  and not self.win_lose_screen.visible 
                  and not self.pause_screen.visible
                  and not self.end_game
                  and event.type == pygame.MOUSEBUTTONDOWN):
                if event.button == 1:
                    #print(self.game_data)
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

                    # switch tên đang hiển thị
                    self.text_switcher.switch()
                    
                    # âm thanh khi bấm chuột
                    self.music_player.click_play()

                    # vẽ cờ lên màn hình
                    self.draw_piece_on(board_x, board_y, cur_piece)

                    # thêm cờ vào bảng
                    self.add_to_history(board_x, board_y)

                    # lưu lại giá trị trong bảng
                    self.game_data['Board'][board_x][board_y] = self.game_data['Turn']
                    
                    
                    
                    # kiểm tra đã thắng chưa
                    self.check_process(board_x, board_y)
                    
                    # if self.win_checker.check_win(self.game_data['Board'], self.game_data['Turn'], board_x, board_y):
                    #     # Save game trước khi làm việc khác
                    #     #game_data = save_manager.SaveManager('game_data.json', 'data').refresh()
                    #     self.game_data['PlayerName']['Player1'] = self.player_1
                    #     self.game_data['PlayerName']['Player2'] = self.player_2
                    #     self.game_data["GameEnded"] = True
                    #     #print(self.game_data)
                    #     save_manager.SaveManager('game_data.json', 'data').save(self.game_data)
                    #     win_player_name = self.player_1 if self.game_data['Turn'] == 1 else self.player_2
                    #     self.win_lose_screen.set_name(win_player_name)
                    #     self.win_lose_screen.show()
                    #     self.btn_play_again.show()
                    #     self.btn_menu.show()
                    #     # self.win_lose_screen.run()
                        
                    # Thay đổi Turn ở cuối mỗi lượt
                    self.game_data['Turn'] = 1 - self.game_data['Turn']

                    # thay đổi turn
                    self.turn = 1 - self.turn
                    
            
            # nếu người dùng bấm thoát
            # if event.type == pygame.QUIT:
            #     # save game trước khi thoát
            #     #print(self.game_data)
            #     self.save_manager.save(self.game_data)
            #     pygame.quit()
            #     sys.exit()

        # nếu không có sự kiện gì thì trả về -1
        # return -1
    
    def run(self):
        #self.exit_screen_created = False
        #self.winlose_window_created = False
        #self.blocked = False
        while self.running_mode == "game":
            # 120 FPS
            time_delta = self.clock.tick(120) / 1000.0
            
            self.screen.blit(self.background_surface, (0,0))
            
            self.continue_game()

            self.loop_on()

            self.text_switcher.draw_on(int(self.options.resolution[0] - 250), 150)
            self.cursor_trail.draw_on(self.screen)
            
            # vẽ pop-up window sau cùng sẽ giúp nó đè lên trên các hình các, tránh bug text_switcher che mất window
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            
            # cập nhật display
            pygame.display.update()
        return self.running_mode
        # pygame.quit()
        # sys.exit()
