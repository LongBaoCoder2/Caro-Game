import pygame, json, pygame_gui, sys
from lib import button, color, save_manager
import game

from subwindow import *
import menu
from lib.paint import Paint
# from winlose import WinLose



class Name:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, screen, gamemode: str):
        pygame.display.set_caption('PLAYER NAME')
        
        # Import DATA
        self.setting = json.load(open('data/setting.json'))
        self.game_data = json.load(open('data/game_data.json'))


        # LOAD DATA
        self.SCREEN_WIDTH  = self.setting['screen']['width']
        self.SCREEN_HEIGHT = self.setting['screen']['height']
        self.PLAYER_NAME = self.game_data["PlayerName"]
        
        # Lưu game mode thành biến của cả class
        self.gamemode = gamemode

        # https://www.programiz.com/python-programming/json
        # dump gamemode vào setting.json
        self.setting["gamemode"] = gamemode
        json.dump(self.setting, open('data/setting.json', 'w'), indent = 4)

        self.screen = screen
        
        self.paint = Paint(self.screen)


        # Load từ data / Nếu không có hoặc new game thì load từ Input
        # self.play_one = self.PLAYER_NAME["Player1"]
        # self.play_two = self.PLAYER_NAME["Player2"]
        # Khởi tạo tên rỗng để tránh bug từ việc lấy dữ liệu từ game cũ lên
        self.play_one = ''
        self.play_two = ''


        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        
        self.clock = pygame.time.Clock()

        self.options = Options(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)    

        # Tạo một manager UI (Quản lý Giao diện màn hình)
        # Tham số truyền vào sẽ là kích thước màn hình và package
        # Hãy xem manager như là một người quản lý màn hình:
        # Với công việc là set up background và vẽ button quản lý các hiệu ứng v.v
        self.manager = pygame_gui.UIManager(self.options.resolution, 
                                            pygame_gui.PackageResource(package='themes',
                                                            resource='theme.json'))



        # # Import Font
        # self.manager.preload_fonts([{ 'point_size': 20, 'style': 'bold'},
        #                             { 'point_size': 20, 'style': 'regular'},
        #                             { 'point_size': 20, 'style': 'italic'},
        #                             { 'point_size': 28, 'style': 'italic'},
        #                             { 'point_size': 28, 'style': 'bold'}
        #                             ])

        self.running = True

        # Tạo background 
        self.background_surface = None

        # Tạo text input để nhập tên
        self.name_player_one = None
        self.name_player_two = None

        # Tạo Button Play để bắt đầu trò chơi
        self.btn_play = None
        self.btn_back = None

        # Thiết kế giao diện
        self.name_message_one = None
        self.name_message_two = None
        self.label = None


        # Gọi hàm để cập nhật UI sẽ được setup bằng pygame_gui
        self.update_ui()    

    def update_ui(self):

        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.manager.get_theme().get_colour("dark_bg"))


        self.btn_size = (int(self.options.resolution[0] * 0.4), int(self.options.resolution[1] * 0.1))
        self.text_entry_size = (int(self.options.resolution[0] * 0.6) , int(self.options.resolution[1] * 0.1))
        self.label_size = (int(self.options.resolution[0] * 0.6), int(self.options.resolution[1] * 0.25))
        
        if (self.gamemode == "Bot"):
            self.name_message_bot = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0] / 2 - self.text_entry_size[0] / 3.5),
                                                            int(self.options.resolution[1] / 2) - 200), self.btn_size),
                                                            text="BOT", 
                                                            manager=self.manager,
                                                            object_id="#name_message")
        else:    
            self.name_player_one = pygame_gui.elements.UITextEntryLine(pygame.Rect((int(self.options.resolution[0] / 2 - self.text_entry_size[0] / 3.5),
                                                                                int(self.options.resolution[1] / 2) - 200), self.text_entry_size),
                                                                    manager = self.manager,
                                                                    object_id="#text_entry")

        self.name_player_two = pygame_gui.elements.UITextEntryLine(pygame.Rect((int(self.options.resolution[0] / 2 - self.text_entry_size[0] / 3.5),
                                                                                int(self.options.resolution[1] / 2) - 100), self.text_entry_size),
                                                                    manager = self.manager,
                                                                    object_id="#text_entry")
        
        self.name_message_one = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0]/2 - self.btn_size[0]*1.3),
                                                            int(self.options.resolution[1] / 2) - 200), self.btn_size),
                                                            text="PLAYER X:", 
                                                            manager=self.manager,
                                                            object_id="#name_message")

        self.name_message_two = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0]/2 - self.btn_size[0]*1.3),
                                                            int(self.options.resolution[1] / 2) - 100), self.btn_size),
                                                            text="PLAYER O:", 
                                                            manager=self.manager,
                                                            object_id="#name_message")

        self.label = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0]* 1.3),
                                                        int(self.options.resolution[1] / 2 - 400)), self.label_size),
                                                            text="ENTER PLAYER NAME", 
                                                            manager=self.manager,
                                                            object_id="#label")

        self.btn_play = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 + 50)), self.btn_size),
                                                        "PLAY",
                                                        self.manager,
                                                        object_id="#all_button")

        self.btn_back = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 + 200)), self.btn_size),
                                                        "BACK",
                                                        self.manager,
                                                        object_id="#all_button")

        # Tạo animation cho chữ
        self.label.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)

        

    def process_events(self):
        for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            #     pygame.quit()
            #     sys.exit()
            # Quản lý và xử lý các sự kiện (như click, hover, ...)
            self.manager.process_events(event)

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if self.gamemode == "PvP": # Chỉ lấy input tên player one nếu chơi chế độ PvP
                    self.play_one = self.name_player_one.get_text()
                else:
                    self.play_one = 'BOT'
                
                self.play_two = self.name_player_two.get_text()

            # if event.type == pygame_gui.UI_B:
            #     if event.ui_element == self.name_player_one and event.ui_element == self.name_player_two:
            #         # play()
            #         pass
            
    
            quit_button_pressed = (event.type == pygame.QUIT)
            if quit_button_pressed or event.type == pygame_gui.UI_BUTTON_PRESSED:
                # chiều rộng (ngang) cửa sổ settings, quit
                sub_window_width = self.options.resolution[0] * 5 // 8
                # chiều cao (dọc) cửa sổ settings, quit
                sub_window_height = self.options.resolution[1] * 5 // 8
                
                if quit_button_pressed:
                    self.exit_screen_created = True
                    self.exit_screen = ExitWindow(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2 - 50),
                                                        int(self.options.resolution[1] / 2) - 125), 
                                                        (sub_window_width * 3 // 4, sub_window_height * 3 // 5)),
                                                        self.manager, self.options.resolution[0], self.options.resolution[1])
                
                #self.exit_screen_created = quit_button_pressed or btn_quit_clicked
                # print(self.exit_screen_created)
                
                elif not quit_button_pressed and self.exit_screen_created:
                    if event.ui_element == self.exit_screen.btn_Exit:
                        #print("Hello")
                        self.running = False
                        break
                            
                    if event.ui_element == self.exit_screen.btn_continue:
                        self.exit_screen.hide()
                        self.exit_screen_created = False
                
                elif event.ui_element == self.btn_back:
                    menu.Menu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT).run()
                
                elif self.play_one != '' and self.play_two != '':
                    game_data = save_manager.SaveManager('game_data.json', 'data').refresh()
                    game_data['PlayerName']['Player1'] = self.play_one
                    game_data['PlayerName']['Player2'] = self.play_two
                    save_manager.SaveManager('game_data.json', 'data').save(game_data)
                    print("> ", self.play_one)
                    print("> ", self.play_two)
                    self.game_screen = game.Game(self.screen)
                    #self.game_screen.new_game()
                    self.game_screen.run()
                        
                        
    def run(self):
        self.exit_screen_created = False
        while self.running:
            # 120 FPS
            time_delta = self.clock.tick(120)

            self.process_events()

            self.screen.blit(self.background_surface, (0,0))
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            pygame.display.update()
        pygame.quit()
        sys.exit()
    
