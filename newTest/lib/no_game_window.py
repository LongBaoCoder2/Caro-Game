import pygame, json, pygame_gui, sys
import lib.button, lib.color, lib.save_manager, lib.options
   
class NoGameWindow(pygame_gui.elements.UIWindow):
    """class NoGameWindows là class kế thừa (Inheritance) từ class pygame_gui.elements.UIWindow

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
                         window_display_title='No game available',
                         object_id='#setting_window',
                         resizable=True)

        self.options = lib.options.Options(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.btn_size = (int(self.rect.width * 0.4), int(self.rect.height * 0.2))
        self.quit_size = (int(self.rect.width * 0.8), int(self.rect.height * 0.2))

        self.is_blocking = True  # blocks all clicking events from interacting beyond this window

        # Setting quit
        # Dòng chữ "quit"
        self.quit_label = pygame_gui.elements.UILabel(pygame.Rect((40,
                                                        int(self.rect.height / 2 - 125)),
                                                        self.quit_size),
                                                        "The last game is over, please start a new game!",
                                                        self.ui_manager,
                                                        container=self)
        self.btn_Back = pygame_gui.elements.UIButton(pygame.Rect((int(self.rect.width / 20) + 150,
                                                        int(self.rect.height / 2 - self.btn_size[1] + 50)),
                                                        self.btn_size),
                                                        "Back",
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