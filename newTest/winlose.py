import pygame, pygame_gui, sys, menu

from lib.paint import Paint
from subwindow import *
import menu

class WinLoseWindow(pygame_gui.elements.UIWindow):
    def __init__(self, rect, ui_manager,SCREEN_WIDTH, SCREEN_HEIGHT, win_player_name):
        super().__init__(rect, ui_manager,
                         window_display_title='Victory',
                         object_id='#win_lose_window',
                         resizable=False)

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        self.options = Options(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.btn_size = ( int(self.rect.width *0.4), 55 )
        self.win_lose_label = (300, 100)
        self.win_player_name = win_player_name

        self.win_image = pygame.image.load("./res/images/win_lose/Win-1.png").convert_alpha()
        self.win_image = pygame.transform.scale(self.win_image, (int(self.SCREEN_WIDTH/5),
                                                                int(self.SCREEN_WIDTH/5)))
        

        self.win_image_ui = None
        self.win_lose_message = None
        self.btn_back = None
        self.btn_continue = None

        self.update_ui()

    def update_ui(self):
        self.win_image_ui = pygame_gui.elements.UIImage(pygame.Rect((int(self.rect.width/3.1),
                                                        int(self.rect.height * 0.2)),
                                                        self.win_image.get_rect().size),
                                                        self.win_image, self.ui_manager,
                                                        container=self)

        self.win_lose_message = pygame_gui.elements.UILabel(pygame.Rect((int(self.rect.width/2 - self.win_lose_label[0]/1.8), 0),
                                                            self.win_lose_label),
                                                            self.win_player_name,
                                                            self.ui_manager,
                                                            container=self,
                                                            object_id="#all_button")

        self.btn_back = pygame_gui.elements.UIButton(pygame.Rect((int(self.rect.width/2 - self.btn_size[0] / 1.8),
                                                        int(self.rect.height * 5 // 8 + self.btn_size[1])), 
                                                        self.btn_size),
                                                        "BACK",
                                                        self.ui_manager,
                                                        object_id="#all_button",
                                                        container=self)

        
                                


    def update(self, time_delta):
        super().update(time_delta)

    def set_name(self, name):
        self.current_name = name
        self.win_lose_message.set_text(self.current_name)
        
        
    def process_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_back:
                self.hide()

        # Quản lý và xử lý các sự kiện (như click, hover, ...)
        self.ui_manager.process_events(event)

class WinLose:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, screen):
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        
        self.paint = Paint(self.screen)
        self.clock = pygame.time.Clock()

        self.options = menu.Options(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)    

        self.manager_win_lose = pygame_gui.UIManager(self.options.resolution, 
                                                    pygame_gui.PackageResource(package='themes',
                                                    resource='theme.json'))   

        # Import Font
        self.manager_win_lose.preload_fonts([{ 'point_size': 20, 'style': 'bold'},
                                    { 'point_size': 20, 'style': 'regular'},
                                    { 'point_size': 20, 'style': 'italic'},
                                    { 'point_size': 28, 'style': 'italic'},
                                    { 'point_size': 28, 'style': 'bold'}
                                    ])

        self.running = True

        self.win_image = pygame.image.load("./res/images/win_lose/Win-1.png").convert_alpha()
        self.win_image = pygame.transform.scale(self.win_image, (self.SCREEN_WIDTH/3, self.SCREEN_WIDTH/3))
    
        self.win_image_rect = self.win_image.get_rect(center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2))


        # Tạo background 
        self.background_surface = None
        self.menu_screen = None

        # Tạo text input để nhập tên
        self.name_player_one = None
        self.name_player_two = None

        # Tạo Button Play để bắt đầu trò chơi
        self.btn_back = None
        self.btn_continue = None

        # Thiết kế giao diện
        self.label = None


        # Gọi hàm để cập nhật UI sẽ được setup bằng pygame_gui
        self.update_ui()    

    def update_ui(self):

        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.manager_win_lose.get_theme().get_colour("dark_bg"))

        
        self.btn_size = (int(self.options.resolution[0] * 0.3), int(self.options.resolution[1] * 0.1))
        self.label_size = (int(self.options.resolution[0] * 0.6), int(self.options.resolution[1] * 0.25))




        self.btn_back = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0] / 2 - self.btn_size[0] - 50),
                                                        int(self.options.resolution[1] / 2 + 150)), self.btn_size),
                                                        "BACK",
                                                        self.manager_win_lose,
                                                        object_id="#all_button")
                                
        self.btn_continue = pygame_gui.elements.UIButton(pygame.Rect((int(self.options.resolution[0]/2 + 50),
                                                        int(self.options.resolution[1] / 2 + 150)), self.btn_size),
                                                        "CONTINUE",
                                                        self.manager_win_lose,
                                                        object_id="#all_button")



        self.label = pygame_gui.elements.UILabel(pygame.Rect((int(self.options.resolution[0] / 2 - self.label_size[0]/2),
                                                        int(self.options.resolution[1] / 2 - 250)), self.label_size),
                                                            text="YOU WIN", 
                                                            manager=self.manager_win_lose,
                                                            object_id="#label")


        # Tạo animation cho chữ
        self.label.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)

        

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.btn_back:
                    # print(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                    menu.Menu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT).run()

            # Quản lý và xử lý các sự kiện (như click, hover, ...)
            self.manager_win_lose.process_events(event)
   
    def run(self):
        while self.running:
            time_delta = self.clock.tick(120)
            self.screen.blit(self.background_surface, (0,0))
            self.paint.render_surface(self.win_image, self.win_image_rect)

            self.process_events()
            
            self.manager_win_lose.update(time_delta)
            self.manager_win_lose.draw_ui(self.screen)

            pygame.display.update()