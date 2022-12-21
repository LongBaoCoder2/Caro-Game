import pygame
from . import color

class CursorTrail:
    
    def __init__(self):
        self.pos_list = []
        self.max_size = 20

    # update vị trí của chuột
    def update_pos(self):

        # thêm vị trí hiện tại của chuột vào list
        self.pos_list.append(pygame.mouse.get_pos())

        # nếu độ dài của list vượt quá giới hạn
        if len(self.pos_list) > self.max_size:

            # xoá vị trí cũ nhất trong list
            del self.pos_list[0]
    
    def draw_on(self, screen):

        # update
        self.update_pos()

        # duyệt qua các vị trí chuột
        for i in range(len(self.pos_list)):

            # vẽ hình tròn theo lịch sử vị trí chuột trong list
            pygame.draw.circle(screen, color.RED, self.pos_list[i], i // 2)
