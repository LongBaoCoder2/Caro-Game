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