import pygame, json, pygame_gui, sys
from lib import button, color, save_manager
import game

from lib.paint import Paint
import subwindow

class PauseWindow(pygame_gui.elements.UIWindow):
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
                         window_display_title='PAUSE',
                         object_id='#setting_window',
                         resizable=True)

        self.options = subwindow.Options(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.btn_size = (int(self.rect.width * 0.4), int(self.rect.height * 0.2))
        self.quit_size = (int(self.rect.width * 0.8), int(self.rect.height * 0.2))

        self.is_blocking = True  # blocks all clicking events from interacting beyond this window

        # Setting quit
        # Dòng chữ "quit"
        self.quit_label = pygame_gui.elements.UILabel(pygame.Rect((int((self.rect.width - self.quit_size[0]) // 2 - 20),
                                                        int(self.rect.height / 2 - 125)),
                                                        self.quit_size),
                                                        "GAME PAUSED",
                                                        self.ui_manager,
                                                        container=self)
        self.btn_Resume = pygame_gui.elements.UIButton(pygame.Rect((int(self.rect.width / 20),
                                                        int(self.rect.height / 2 - self.btn_size[1] + 50)),
                                                        self.btn_size),
                                                        "RESUME",
                                                        self.ui_manager,
                                                        container=self,
                                                        object_id="#all_button")
        
        self.btn_menu = pygame_gui.elements.UIButton(pygame.Rect((int(self.rect.width / 20 + self.btn_size[0] + 20),
                                                        int(self.rect.height / 2 - self.btn_size[1] + 50)), 
                                                        self.btn_size),
                                                        "MENU",
                                                        self.ui_manager,
                                                        container=self,
                                                        object_id="#all_button")
    def on_close_window_button_pressed(self):
        """
        Override this method to call 'hide()' instead if you want to hide a window when the
        close button is pressed.
        """
        # self.kill()
        self.hide()