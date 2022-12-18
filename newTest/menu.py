import pygame, json, pygame_gui, sys
from lib import button, color
import game


setting = json.load(open('data/setting.json'))
SCREEN_WIDTH  = setting['screen']['width']
SCREEN_HEIGHT = setting['screen']['height']


class Options:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)   # Kích thước
        # self.fullscreen = False                         # Toàn màn hình


class Name:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, screen):

        self.game_screen = game.Game()
        # Load từ data / Nếu không có hoặc new game thì load từ Input
        self.play_one = ''
        self.play_two = ''


        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        self.screen = screen
        
        self.clock = pygame.time.Clock()

        self.options = Options(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)    

        self.manager_name = pygame_gui.UIManager(self.options.resolution, 
                                                    pygame_gui.PackageResource(package='themes',
                                                    resource='theme.json'))   



        # Import Font
        self.manager_name.preload_fonts([{ 'point_size': 20, 'style': 'bold'},
                                    { 'point_size': 20, 'style': 'regular'},
                                    { 'point_size': 20, 'style': 'italic'},
                                    { 'point_size': 28, 'style': 'italic'},
                                    { 'point_size': 28, 'style': 'bold'}
                                    ])

        self.running = True
        self.background_surface = None
        self.name_player_one = None
        self.name_player_two = None
        self.btn_play = None

        self.update_ui()    

    def update_ui(self):

        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.manager_name.get_theme().get_colour("dark_bg"))


        self.btn_size = (int(self.options.resolution[0] * 0.4), int(self.options.resolution[1] * 0.1))
        self.text_entry_size = (int(self.options.resolution[0] * 0.5) , int(self.options.resolution[1] * 0.1))
        
        self.name_player_one = pygame_gui.elements.UITextEntryLine(pygame.Rect((int(self.options.resolution[0] / 2 - self.text_entry_size[0] / 2),
                                                                                int(self.options.resolution[1] / 2 - 100)), self.text_entry_size),
                                                                    manager = self.manager_name,
                                                                    object_id="#text_entry")

        self.name_player_two = pygame_gui.elements.UITextEntryLine(pygame.Rect((int(self.options.resolution[0] / 2 - self.text_entry_size[0] / 2),
                                                                                int(self.options.resolution[1] / 2)), self.text_entry_size),
                                                                    manager = self.manager_name,
                                                                    object_id="#text_entry")
        
        self.btn_play = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 + 100)), self.btn_size),
                                                        "PLAY",
                                                        self.manager_name,
                                                        object_id="#all_button")
    # DEBUG:
    def show(self, text1 , text2):
        print(f"Hello {text1} and {text2}")


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
                    self.game_screen.new_game(self.screen)
                    while True:
                        self.game_screen.loop_on(self.screen)
   
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
        

        self.game_screen = game.Game()
        # Khởi tạo option settings (Kích thước và toàn màn hình)
        self.options = Options(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Khởi tạo toàn màn hình
        # if self.options.fullscreen:
        #     self.screen = pygame.display.set_mode(self.options.resolution, pygame.FULLSCREEN)
        # else:
        #     self.screen = pygame.display.set_mode(self.options.resolution)
        
        self.screen = pygame.display.set_mode(self.options.resolution)


        # Tạo một manager UI (Quản lý Giao diện màn hình)
        # Tham số truyền vào sẽ là kích thước màn hình và package
        # Hãy xem manager như là một người quản lý màn hình:
        # Với công việc là set up background và vẽ button quản lý các hiệu ứng v.v
        self.manager = pygame_gui.UIManager(self.options.resolution, 
                                            pygame_gui.PackageResource(package='themes',
                                                            resource='theme.json'))

        # Import Fonts                                                        
        self.manager.preload_fonts([{ 'point_size': 20, 'style': 'bold'},
                                    { 'point_size': 20, 'style': 'regular'},
                                    { 'point_size': 20, 'style': 'italic'},
                                    { 'point_size': 28, 'style': 'italic'},
                                    { 'point_size': 28, 'style': 'bold'}
                                    ])

        # Màn hình Nhập Tên người chơi
        self.name_screen = None



        self.running = True
        
        # Tạo background (sẽ setup sau)
        self.background_surface = None

        # Tạo Title Game
        self.title_game_caro = None

        # Tạo Button
        self.btn_play = None
        self.btn_continue = None
        self.btn_settings = None

        # Tạo Box Setting
        self.settings_window = None

        # Dropdown Box Setting size
        self.setting_resolution = None

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
        
        
        self.title_game_caro = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0] / 2 - self.label_size[0] / 2),
                                                        int(self.options.resolution[1] / 2 - 250)), self.label_size),
                                                        "GAME CARO",
                                                        manager=self.manager,
                                                        object_id="#label")
        
        # Kích thước 
        current_resolution = f"{self.options.resolution[0]}x{self.options.resolution[1]}"
        
        
        self.size_arr = ['640x480', '800x600', '1024x768']
        self.setting_resolution = pygame_gui.elements.UIDropDownMenu(self.size_arr,
                                             current_resolution,
                                             pygame.Rect((int(self.options.resolution[0] * 0.7),
                                                        int(self.options.resolution[1] * 0.8)),
                                                         (200, 25)),
                                             self.manager)

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

                if event.ui_element == self.btn_continue:
                    self.game_screen.continue_game(self.screen)
                    while True:
                        self.game_screen.loop_on(self.screen)


            if (event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
                    and event.ui_element == self.setting_resolution):
                self.change_size(event.text)

    def run(self):
        while self.running:
            time_delta = self.clock.tick() / 1000.0

            self.process_events()

            self.screen.blit(self.background_surface, (0,0))
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.update()
