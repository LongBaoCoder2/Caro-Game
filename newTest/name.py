import pygame, json, pygame_gui, sys
from lib import button, color, save_manager
import game

from subwindow import *
from lib.paint import Paint
# from winlose import WinLose


# Import DATA
setting = json.load(open('data/setting.json'))
game_data = json.load(open('data/game_data.json'))


# LOAD DATA
SCREEN_WIDTH  = setting['screen']['width']
SCREEN_HEIGHT = setting['screen']['height']
PLAYER_NAME = game_data["PlayerName"]

class Name:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, screen, gamemode: str):
        # Lưu game mode thành biến của cả class
        self.gamemode = gamemode

        self.screen = screen
        
        self.paint = Paint(self.screen)


        # Load từ data / Nếu không có hoặc new game thì load từ Input
        self.play_one = PLAYER_NAME["Player1"]
        self.play_two = PLAYER_NAME["Player2"]


        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        
        self.clock = pygame.time.Clock()

        self.options = Options(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)    

        # Tạo một manager UI (Quản lý Giao diện màn hình)
        # Tham số truyền vào sẽ là kích thước màn hình và package
        # Hãy xem manager như là một người quản lý màn hình:
        # Với công việc là set up background và vẽ button quản lý các hiệu ứng v.v
        self.manager_name = pygame_gui.UIManager(self.options.resolution, 
                                            pygame_gui.PackageResource(package='themes',
                                                            resource='theme.json'))



        # # Import Font
        # self.manager_name.preload_fonts([{ 'point_size': 20, 'style': 'bold'},
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

        # Thiết kế giao diện
        self.name_message_one = None
        self.name_message_two = None
        self.label = None


        # Gọi hàm để cập nhật UI sẽ được setup bằng pygame_gui
        self.update_ui()    

    def update_ui(self):

        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.manager_name.get_theme().get_colour("dark_bg"))


        self.btn_size = (int(self.options.resolution[0] * 0.4), int(self.options.resolution[1] * 0.1))
        self.text_entry_size = (int(self.options.resolution[0] * 0.6) , int(self.options.resolution[1] * 0.1))
        self.label_size = (int(self.options.resolution[0] * 0.6), int(self.options.resolution[1] * 0.25))
        
        if (self.gamemode == "Bot"):
            self.name_message_bot = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0] / 2 - self.text_entry_size[0] / 3.5),
                                                            int(self.options.resolution[1] / 2 - 100)), self.btn_size),
                                                            text="BOT", 
                                                            manager=self.manager_name,
                                                            object_id="#name_message")
        else:    
            self.name_player_one = pygame_gui.elements.UITextEntryLine(pygame.Rect((int(self.options.resolution[0] / 2 - self.text_entry_size[0] / 3.5),
                                                                                int(self.options.resolution[1] / 2 - 100)), self.text_entry_size),
                                                                    manager = self.manager_name,
                                                                    object_id="#text_entry")

        self.name_player_two = pygame_gui.elements.UITextEntryLine(pygame.Rect((int(self.options.resolution[0] / 2 - self.text_entry_size[0] / 3.5),
                                                                                int(self.options.resolution[1] / 2)), self.text_entry_size),
                                                                    manager = self.manager_name,
                                                                    object_id="#text_entry")
        
        self.btn_play = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 + 150)), self.btn_size),
                                                        "PLAY",
                                                        self.manager_name,
                                                        object_id="#all_button")
    
        self.name_message_one = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0]/2 - self.btn_size[0]*1.3),
                                                            int(self.options.resolution[1] / 2 - 100)), self.btn_size),
                                                            text="PLAYER X:", 
                                                            manager=self.manager_name,
                                                            object_id="#name_message")

        self.name_message_two = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0]/2 - self.btn_size[0]*1.3),
                                                            int(self.options.resolution[1] / 2)), self.btn_size),
                                                            text="PLAYER O:", 
                                                            manager=self.manager_name,
                                                            object_id="#name_message")

        self.label = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0]* 1.3),
                                                        int(self.options.resolution[1] / 2 - 250)), self.label_size),
                                                            text="SETTINGS", 
                                                            manager=self.manager_name,
                                                            object_id="#label")


        # Tạo animation cho chữ
        self.label.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)

        

    def process_events(self):
        for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            #     pygame.quit()
            #     sys.exit()
            # Quản lý và xử lý các sự kiện (như click, hover, ...)
            self.manager_name.process_events(event)

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
                                                        self.manager_name, self.options.resolution[0], self.options.resolution[1])
                
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
   
                elif self.play_one != '' and self.play_two != '':
                    game_data = save_manager.SaveManager('game_data.json', 'data').refresh()
                    game_data['PlayerName']['Player1'] = self.play_one
                    game_data['PlayerName']['Player2'] = self.play_two
                    save_manager.SaveManager('game_data.json', 'data').save(game_data)
                    print("> ", self.play_one)
                    print("> ", self.play_two)
                    self.game_screen = game.Game(self.screen)
                    self.game_screen.new_game()
                    while True:
                        self.game_screen.run(self.gamemode)
                        
                        
    def run(self):
        self.exit_screen_created = False
        while self.running:
            # 120 FPS
            time_delta = self.clock.tick(120)

            self.process_events()

            self.screen.blit(self.background_surface, (0,0))
            self.manager_name.update(time_delta)
            self.manager_name.draw_ui(self.screen)

            pygame.display.update()
        pygame.quit()
        sys.exit()
    
