import pygame
from . import color

class TextSwitcher:
    
    def __init__(self, screen, bg_color, player):

        self.screen   = screen
        self.bg_color = bg_color
        self.font     = pygame.font.SysFont('Consolas', 35)
        self.player   = [self.font.render(player[0], True, color.WHITE), self.font.render(player[1], True, color.WHITE)]
        self.turn     = 0
        self.v_y      = 0
        self.d_y      = 0
    
    def switch(self):

        # thay đổi vận tốc
        if self.turn == 0:
            self.v_y = 3.5
        else:
            self.v_y = -3.5

        # đổi turn
        self.turn = 1 - self.turn

    def draw_on(self, x, y):

        # thay đổi delta theo vận tốc
        self.d_y += self.v_y
        
        # nếu vượt quá giới hạn thì gán vận tốc bằng 0
        if (self.d_y <= 0 or self.d_y >= 35):
            self.v_y = 0

        # vẽ hình chữ nhật làm nền
        pygame.draw.rect(self.screen, (self.bg_color), (x, y, 200, 105))

        # vẽ tên 2 người chơi
        self.screen.blit(self.player[0], (x, y + self.d_y))
        self.screen.blit(self.player[1], (x, y + 35 + self.d_y))
        # self.screen.blit(self.player[1], (x, y + 70 + self.d_y))

        # vẽ hai hình chữ nhật che lại
        pygame.draw.rect(self.screen, self.bg_color, (x, y, 220, 35))
        pygame.draw.rect(self.screen, self.bg_color, (x, y + 70, 220, 35))
        # pygame.draw.rect(self.screen, color.BLACK, (x, y, 200, 35))
        # pygame.draw.rect(self.screen, color.BLACK, (x, y + 70, 200, 35))

        # vẽ chữ Play Turn và hình chữ nhật bao quanh tên người chơi
        self.screen.blit(pygame.font.SysFont('Consolas', 25).render('Play Turn:', True, color.WHITE), (x, y))
        delta = 5
        # pygame.draw.rect(self.screen, color.BLACK, (x - delta * 2, y - delta + 35, 220, 35 + delta * 2), 5, 10)
