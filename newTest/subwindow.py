import pygame, json, pygame_gui, sys
from lib import button, color, save_manager
import game

from lib.paint import Paint
#from name import *
#from menu import *
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
        self.resolution_drop_down = pygame_gui.elements.UIDropDownMenu(['640x480', '800x600', '1024x768', '1280x960'],
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
        self.btn_size = (int(self.rect.width * 0.4), int(self.rect.height * 0.2))
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