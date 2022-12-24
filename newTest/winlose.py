import pygame, pygame_gui, sys, menu

from lib.paint import Paint
import menu


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
                    print(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
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