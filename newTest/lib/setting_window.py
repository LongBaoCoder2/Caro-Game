import pygame, json, pygame_gui, sys
import lib.button, lib.color, lib.save_manager, lib.options

#from lib.paint import Paint
#from name import *
#from menu import *
# from winlose import WinLose

# # Import DATA
# setting = json.load(open('data/setting.json'))
# game_data = json.load(open('data/game_data.json'))


# # LOAD DATA
# SCREEN_WIDTH  = setting['screen']['width']
# SCREEN_HEIGHT = setting['screen']['height']
# PLAYER_NAME = game_data["PlayerName"]


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
        
        # Import DATA
        self.setting = json.load(open('data/setting.json'))
        self.game_data = json.load(open('data/game_data.json'))

        self.is_blocking = True  # blocks all clicking events from interacting beyond this window
        
        # LOAD DATA
        self.SCREEN_WIDTH  = self.setting['screen']['width']
        self.SCREEN_HEIGHT = self.setting['screen']['height']
        PLAYER_NAME = self.game_data["PlayerName"]
        
        # list chứa các giá trị hiện trong menu drop down 
        self.pieces_mode = ['3', '4', '5', '6']
        self.pieces_mode_pos = -1
        self.board_size = [
            ['3x3'],
            ['10x10', '12x12'],
            ['16x16', '20x20'],
            ['20x20', '24x24']
        ]
        self.resolution = ['640x480', '800x600', '1024x768', '1280x960']

        self.options = lib.options.Options(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.btn_size = ( int(self.rect.width *0.6), 30 )

        # Số quân liên tiếp cần để thắng
        self.pieces_mode_label = pygame_gui.elements.UILabel(pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 - 250)),
                                                            self.btn_size),
                                                            "Số quân liên tiếp để thắng: ",
                                                            self.ui_manager,
                                                            container=self)
        # Lấy giá trị của số quân liên tiếp để thắng
        self.current_pieces_mode = (str(self.setting["game"]["win_cnt"]))
        
         
        # Dòng này hiện ra menu xổ xuống của số quân liên tiếp cần để thắng
        self.pieces_mode_drop_down = pygame_gui.elements.UIDropDownMenu(self.pieces_mode,
                                                  self.current_pieces_mode,
                                                  pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 - 200)),
                                                            self.btn_size),
                                                  self.ui_manager,
                                                  container=self)
        
        # Kích cỡ bàn cờ
        self.pieces_mode_label = pygame_gui.elements.UILabel(pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 - 150)),
                                                            self.btn_size),
                                                            "Board size: ",
                                                            self.ui_manager,
                                                            container=self)
        # Lấy giá trị của kích cỡ bàn cờ hiện tại
        self.current_board_size = (str(self.setting["grid"]["size_x"]) 
                                   + 'x' 
                                   + str(self.setting["grid"]["size_y"]))
        
        self.pieces_mode_pos = self.pieces_mode.index(self.pieces_mode_drop_down.selected_option)
        # self.update_pieces_mode_index() 
        # Dòng này hiện ra menu xổ xuống của kích cỡ bàn cờ
        self.board_size_drop_down = pygame_gui.elements.UIDropDownMenu(self.board_size[self.pieces_mode_pos],
                                                  self.current_board_size,
                                                  pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 - 100)),
                                                            self.btn_size),
                                                  self.ui_manager,
                                                  container=self)
        
        # Độ phân giải
        self.resolution_label = pygame_gui.elements.UILabel(pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 - 50)),
                                                            self.btn_size),
                                                            "Resolution: ",
                                                            self.ui_manager,
                                                            container=self)
        # Lấy giá trị của độ phân giải màn hình hiện tại
        self.current_resolution_string = (str(self.options.resolution[0]) +
                                     'x' +
                                     str(self.options.resolution[1]))
        
        # Dòng này hiện ra menu xổ xuống
        self.resolution_drop_down = pygame_gui.elements.UIDropDownMenu(self.resolution,
                                                  self.current_resolution_string,
                                                  pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 + 0)),
                                                            self.btn_size),
                                                  self.ui_manager,
                                                  container=self)

        # Setting Volume
        # Dòng chữ "Volume"
        self.volume_label = pygame_gui.elements.UILabel(pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 + 50)),
                                                            self.btn_size),
                                                            "Volume: ",
                                                            self.ui_manager,
                                                            container=self)
        # Thanh trượt qua lại
        self.volume_settings = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2) + 100),
                                                            self.btn_size),
                                                            50.0,
                                                            (0.0, 100.0),
                                                            self.ui_manager,
                                                            container=self,
                                                            click_increment=5)
            # Âm thanh
        self.current_volume = pygame_gui.elements.UILabel(pygame.Rect((int(self.rect.width / 2 + self.btn_size[0] /2),
                                                int(self.rect.height / 2 + 100)),
                                                (50, 50)),
                                    str(int(self.volume_settings.get_current_value())),
                                    self.ui_manager,
                                    container=self)
    
    # def update_pieces_mode_index(self) -> None:
    #     self.pieces_mode_pos = self.pieces_mode.index(self.pieces_mode_drop_down.selected_option)
    
    def update_board_size_drop_down(self) -> None:
        self.pieces_mode_pos = self.pieces_mode.index(self.pieces_mode_drop_down.selected_option)
        print("bo may co update", self.board_size[self.pieces_mode_pos])
        
        # kill thằng cũ để tạo thằng mới
        self.board_size_drop_down.kill()
        
        self.board_size_drop_down = pygame_gui.elements.UIDropDownMenu(self.board_size[self.pieces_mode_pos],
                                                  self.board_size[self.pieces_mode_pos][0],
                                                  pygame.Rect((int(self.rect.width / 2 - self.btn_size[0] / 2),
                                                            int(self.rect.height / 2 - 100)),
                                                            self.btn_size),
                                                  self.ui_manager,
                                                  container=self)
        print(self.board_size_drop_down.selected_option)
        self.board_size_drop_down.selected_option = self.board_size[self.pieces_mode_pos][0]
    
    def on_close_window_button_pressed(self):
        """
        Override this method to call 'hide()' instead if you want to hide a window when the
        close button is pressed.
        """
        # self.kill()
        self.hide()  

        # self.health_bar = UIScreenSpaceHealthBar(pygame.Rect((int(self.rect.width / 9),
        #                                                       int(self.rect.height * 0.7)),
        #                                                      (200, 30)),
        #                                          self.ui_manager,
        #                                          container=self)

    def update(self, time_delta):
        super().update(time_delta)
        if self.alive() and self.volume_settings.has_moved_recently:
            self.current_volume.set_text(str(int(self.volume_settings.get_current_value())))
            


