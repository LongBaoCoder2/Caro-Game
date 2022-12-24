import pygame, json, pygame_gui, sys
from lib import button, color, save_manager
import game

from lib.paint import Paint
# from winlose import WinLose


# Import DATA
setting = json.load(open('data/setting.json'))
game_data = json.load(open('data/game_data.json'))


# LOAD DATA
SCREEN_WIDTH  = setting['screen']['width']
SCREEN_HEIGHT = setting['screen']['height']
PLAYER_NAME = game_data["PlayerName"]



class Options:
    """
    Khởi tạo game các lựa chọn
    """
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        """ khởi tạo cửa sổ intro

        Args:
            SCREEN_WIDTH (int): độ rộng chiều ngang của của màn hình pygame
            SCREEN_HEIGHT (int): độ cao chiều dọc của màn hình pygame
        """
        self.resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)   # Kích thước
        # self.fullscreen = False                         # Toàn màn hình


class SettingWindow(pygame_gui.elements.UIWindow):
    """class SettingWindow là class kế thừa (Inheritance) từ class pygame_gui.elements.UIWindow

    Args:
        pygame_gui (_type_): _description_
    """
    def __init__(self, rect, ui_manager,SCREEN_WIDTH, SCREEN_HEIGHT):
        """Hàm khởi tạo (constructor)

        Args:
            rect (_type_): _description_
            ui_manager (_type_): _description_
            SCREEN_WIDTH (int): chiều dài (ngang) của cửa sổ
            SCREEN_HEIGHT (int): chiều cao (dọc) của cửa sổ
        """
        super().__init__(rect, ui_manager,
                         window_display_title='Setting',
                         object_id='#setting_window',
                         resizable=True)

        self.options = Options(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.btn_size = ( int(self.rect.width *0.6), 30 )



        # Setting Volume
        # Dòng chữ "Volume"
        self.volume_label = pygame_gui.elements.UILabel(pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 - 0)),
                                                            self.btn_size),
                                                            "Volume: ",
                                                            self.ui_manager,
                                                            container=self)
        # Thanh trượt qua lại
        self.volume_settings = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2) + 50),
                                                            self.btn_size),
                                                            50.0,
                                                            (0.0, 100.0),
                                                            self.ui_manager,
                                                            container=self,
                                                            click_increment=5)
            # Âm thanh
        self.current_volume = pygame_gui.elements.UILabel(pygame.Rect((int(self.rect.width / 2 + self.btn_size[0] /2),
                                                int(self.rect.height / 2 + 50)),
                                                (50, 50)),
                                    str(int(self.volume_settings.get_current_value())),
                                    self.ui_manager,
                                    container=self)

        # Độ phân giải
        self.resolution_label = pygame_gui.elements.UILabel(pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 - 100)),
                                                            self.btn_size),
                                                            "Resolution: ",
                                                            self.ui_manager,
                                                            container=self)
        # Lấy giá trị của độ phân giải màn hình hiện tại
        self.current_resolution_string = (str(self.options.resolution[0]) +
                                     'x' +
                                     str(self.options.resolution[1]))
        # Dòng này hiện ra menu xổ xuống
        self.resolution_drop_down = pygame_gui.elements.UIDropDownMenu(['1280x960'],
                                                  self.current_resolution_string,
                                                  pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 - 50)),
                                                            self.btn_size),
                                                  self.ui_manager,
                                                  container=self)
        
       
        
        # Số quân liên tiếp cần để thắng
        self.pieces_mode_label = pygame_gui.elements.UILabel(pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 - 200)),
                                                            self.btn_size),
                                                            "Số quân liên tiếp để thắng: ",
                                                            self.ui_manager,
                                                            container=self)
        # Lấy giá trị của số quân liên tiếp để thắng
        self.current_pieces_mode = (str(setting["game"]["win_cnt"]))
         
        # Dòng này hiện ra menu xổ xuống của số quân liên tiếp cần để thắng
        self.pieces_mode_drop_down = pygame_gui.elements.UIDropDownMenu(['3', '4', '5', '6'],
                                                  self.current_pieces_mode,
                                                  pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 - 150)),
                                                            self.btn_size),
                                                  self.ui_manager,
                                                  container=self)

        # self.health_bar = UIScreenSpaceHealthBar(pygame.Rect((int(self.rect.width / 9),
        #                                                       int(self.rect.height * 0.7)),
        #                                                      (200, 30)),
        #                                          self.ui_manager,
        #                                          container=self)

    def update(self, time_delta):
        super().update(time_delta)

        if self.alive() and self.volume_settings.has_moved_recently:
            self.current_volume.set_text(str(int(self.volume_settings.get_current_value())))
            
class ExitWindow(pygame_gui.elements.UIWindow):
    """class ExitWindows là class kế thừa (Inheritance) từ class pygame_gui.elements.UIWindow

    Args:
        pygame_gui (_type_): _description_
    """
    def __init__(self, rect, ui_manager,SCREEN_WIDTH, SCREEN_HEIGHT):
        """Hàm khởi tạo (constructor)

        Args:
            rect (_type_): _description_
            ui_manager (_type_): _description_
            SCREEN_WIDTH (int): chiều dài (ngang) của cửa sổ
            SCREEN_HEIGHT (int): chiều cao (dọc) của cửa sổ
        """
        super().__init__(rect, ui_manager,
                         window_display_title='Exit',
                         object_id='#setting_window',
                         resizable=True)

        self.options = Options(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.btn_size = ( int(self.rect.width * 0.4), int(self.rect.height * 0.2))
        self.quit_size = (int(self.rect.width * 0.8), int(self.rect.height * 0.2))



        # Setting quit
        # Dòng chữ "quit"
        self.quit_label = pygame_gui.elements.UILabel(pygame.Rect((int((self.rect.width - self.quit_size[0]) // 2),
                                                        int(self.rect.height / 2 - 125)),
                                                        self.quit_size),
                                                        #"vai lon luon",
                                                        "Are you sure you want to quit the game?",
                                                        self.ui_manager,
                                                        container=self)
        self.btn_Exit = pygame_gui.elements.UIButton(pygame.Rect((int(self.rect.width / 20),
                                                        int(self.rect.height / 2 - self.btn_size[1] + 50)),
                                                        self.btn_size),
                                                        "Exit",
                                                        self.ui_manager,
                                                        container=self,
                                                        object_id="#all_button")
        
        self.btn_continue = pygame_gui.elements.UIButton(pygame.Rect((int(self.rect.width / 20 + self.btn_size[0] + 20),
                                                        int(self.rect.height / 2 - self.btn_size[1] + 50)), 
                                                        self.btn_size),
                                                        "Keep Playing",
                                                        self.ui_manager,
                                                        container=self,
                                                        object_id="#all_button")

    # def update(self, time_delta):
    #     super().update(time_delta)

    #     if self.alive() and self.volume_settings.has_moved_recently:
    #         self.current_volume.set_text(str(int(self.volume_settings.get_current_value())))
    
class Name:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, screen):

        self.screen = screen
        
        self.paint = Paint(self.screen)


        # Load từ data / Nếu không có hoặc new game thì load từ Input
        self.play_one = PLAYER_NAME["Player1"]
        self.play_two = PLAYER_NAME["Player2"]


        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        
        self.clock = pygame.time.Clock()

        self.options = Options(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)    

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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Quản lý và xử lý các sự kiện (như click, hover, ...)
            self.manager_name.process_events(event)

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                self.play_one = self.name_player_one.get_text()
                self.play_two = self.name_player_two.get_text()

            # if event.type == pygame_gui.UI_B:
            #     if event.ui_element == self.name_player_one and event.ui_element == self.name_player_two:
            #         # play()
            #         pass

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if self.play_one != '' and self.play_two != '':
                    game_data = save_manager.SaveManager('game_data.json', 'data').refresh()
                    game_data['PlayerName']['Player1'] = self.play_one
                    game_data['PlayerName']['Player2'] = self.play_two
                    save_manager.SaveManager('game_data.json', 'data').save(game_data)
                    print("> ", self.play_one)
                    print("> ", self.play_two)
                    self.game_screen = game.Game(self.screen)
                    self.game_screen.new_game()
                    while True:
                        self.game_screen.loop_on()
   
    def run(self):
         while self.running:
            time_delta = self.clock.tick() / 1000.0

            self.process_events()

            self.screen.blit(self.background_surface, (0,0))
            self.manager_name.update(time_delta)
            self.manager_name.draw_ui(self.screen)

            pygame.display.update()


class Menu:
    # khởi tạo
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.init()

        self.clock = pygame.time.Clock()
        pygame.display.set_caption('MENU')

        # Khởi tạo option settings (Kích thước và toàn màn hình)
        self.options = Options(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.screen = pygame.display.set_mode(self.options.resolution)

        # Dùng để vẽ các image và render text
        self.paint = Paint(self.screen)



        
        # Khởi tạo toàn màn hình
        # if self.options.fullscreen:
        #     self.screen = pygame.display.set_mode(self.options.resolution, pygame.FULLSCREEN)
        # else:
        #     self.screen = pygame.display.set_mode(self.options.resolution)
        


        # Tạo một manager UI (Quản lý Giao diện màn hình)
        # Tham số truyền vào sẽ là kích thước màn hình và package
        # Hãy xem manager như là một người quản lý màn hình:
        # Với công việc là set up background và vẽ button quản lý các hiệu ứng v.v
        self.manager = pygame_gui.UIManager(self.options.resolution, 
                                            pygame_gui.PackageResource(package='themes',
                                                            resource='theme.json'))

        # Import Fonts                                                        
        # self.manager.preload_fonts([{'name': 'fira_code', 'point_size': 10, 'style': 'bold'},
        #                                {'name': 'fira_code', 'point_size': 10, 'style': 'regular'},
        #                                {'name': 'fira_code', 'point_size': 10, 'style': 'italic'},
        #                                {'name': 'fira_code', 'point_size': 14, 'style': 'italic'},
        #                                {'name': 'fira_code', 'point_size': 14, 'style': 'bold'}
        #                                ])

        # Màn hình Nhập Tên người chơi
        self.name_screen = None

        # Màn hình setting
        self.setting_screen = None

        # Màn hình Quit
        self.quit_screen = None

        self.running = True
        
        # Tạo background (sẽ setup sau)
        self.background_surface = None

        # Tạo Title Game
        self.title_game_caro = None

        # Tạo Button
        self.btn_play = None
        self.btn_continue = None
        self.btn_settings = None
        self.btn_quit = None


        # Thiết kế giao diện
        self.image_list = []
        self.image_position = []

        # Import picture
        for index in range(1,5):
            # Import Image
            image = pygame.image.load(f"./res/images/menu/image-{index}.png").convert_alpha()
            # Apend image_list
            self.image_list.append(image)

        # Tạo Box Setting
        self.settings_window = None

        # Dropdown Box Setting size
        self.setting_resolution = None

        # Tạo Box Quit
        self.quit_window = None
        
        self.update_ui()


    # Hàm cập nhật kích thước màn hình
    def update_ui(self):
        self.manager.set_window_resolution(self.options.resolution)
        self.manager.clear_and_reset()

        self.name_screen = Name(self.options.resolution[0], self.options.resolution[1], self.screen)


        self.btn_size = (int(self.options.resolution[0] * 0.4), int(self.options.resolution[1] * 0.1))
        self.label_size = (int(self.options.resolution[0] * 0.6), int(self.options.resolution[1] * 0.25))
        # Setup Background
        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.manager.get_theme().get_colour("dark_bg"))  # dark_bg nằm trong file theme.json

        # Tạo ra các button ở màn hình Intro
        self.btn_play = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 - 100)), self.btn_size),
                                                        "PLAY",
                                                        self.manager,
                                                        object_id="#all_button")
        
        self.btn_continue = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
                                                        int(self.options.resolution[1] / 2)), self.btn_size),
                                                        "CONTINUE",
                                                        self.manager,
                                                        object_id="#all_button")                                        
        
        self.btn_settings = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 + 100)), self.btn_size),
                                                        "SETTINGS",
                                                        self.manager,
                                                        object_id="#all_button")
        
        self.btn_quit = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 + 200)), 
                                                        self.btn_size),
                                                        "QUIT",
                                                        self.manager,
                                                        object_id="#all_button")
        
        
        self.title_game_caro = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0] / 2 - self.label_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 - 250)), self.label_size),
                                                        text="Game Caro", 
                                                        manager=self.manager,
                                                        object_id="#label")
        

        self.image_position = [(int(self.options.resolution[0] * 0.1), int(self.options.resolution[1] * 0.65)), 
                                (int(self.options.resolution[0] * 0.125), int(self.options.resolution[1] * 0.125)), 
                                (int(self.options.resolution[0] * 0.75), int(self.options.resolution[1] * 0.7)), 
                                (int(self.options.resolution[0] * 0.75), int(self.options.resolution[1] * 0.1))]


        self.title_game_caro.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
        
        
        
        # Kích thước 
        current_resolution = f"{self.options.resolution[0]}x{self.options.resolution[1]}"
        
        
        self.size_arr = ['640x480', '800x600', '1024x768', '1280x960']
        # self.setting_resolution = pygame_gui.elements.UIDropDownMenu(self.size_arr,
        #                                      current_resolution,
        #                                      pygame.Rect((int(self.options.resolution[0] * 0.7),
        #                                                 int(self.options.resolution[1] * 0.8)),
        #                                                  (200, 25)),
        #                                      self.manager,
        #                                      object_id="#drop_down_options_list")

        
    def change_size(self, text):
        resolution_str = text.split('x')
        resolution_width = int(resolution_str[0])
        resolution_height = int(resolution_str[1])
        if (resolution_width != self.options.resolution[0] or
                resolution_height != self.options.resolution[1]):
            self.options.resolution = (resolution_width, resolution_height)
            self.screen = pygame.display.set_mode(self.options.resolution)
            self.update_ui()

    
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Quản lý và xử lý các sự kiện (như click, hover, ...)
            self.manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.btn_play:
                    # Truyền hàm khởi tạo trò chơi vào
                    self.name_screen.run()
                
                # chiều rộng (ngang) cửa sổ settings, quit
                sub_window_width = self.options.resolution[0] * 5 // 8
                # chiều cao (dọc) cửa sổ settings, quit
                sub_window_height = self.options.resolution[1] * 5 // 8
                
                if event.ui_element == self.btn_settings:
                    self.setting_screen = SettingWindow(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2 - 150),
                                                        int(self.options.resolution[1] / 2) - 200), 
                                                        (sub_window_width, sub_window_height)), 
                                                        self.manager, self.options.resolution[0], self.options.resolution[1])
                
                if event.ui_element == self.btn_quit:
                    self.exit_screen = ExitWindow(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2 - 50),
                                                        int(self.options.resolution[1] / 2) - 125), 
                                                        (sub_window_width * 3 // 4, sub_window_height * 3 // 5)),
                                                        self.manager, self.options.resolution[0], self.options.resolution[1])
                
                if event.ui_element == self.btn_continue:
                    self.game_screen = game.Game(self.screen)
                    self.game_screen.continue_game()
                    while True:
                        self.game_screen.loop_on()
                
                if event.ui_element == self.exit_screen.btn_Exit:
                    self.running = False
                    
                if event.ui_element == self.exit_screen.btn_continue:
                    self.exit_screen.hide()


            if (event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
                    and event.ui_element == self.setting_screen.resolution_drop_down):
                self.change_size(event.text)
            

    def run(self):
        """Chạy màn hình game
        """
        while self.running:
            time_delta = self.clock.tick() / 1000.0
            # Vẽ hình nền lên screen
            self.screen.blit(self.background_surface, (0,0))

            # Vẽ các hình mini
            for index in range(4):
                self.paint.render_surface(self.image_list[index], self.image_position[index])

            self.process_events()

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.update()
