import pygame
from . import color

class TextSwitcher:
    
    def __init__(self, screen, bg_color, player):

        self.screen   = screen
        self.bg_color = bg_color
        self.font     = pygame.font.SysFont('Consolas', 35)
        self.player   = [self.font.render(player[0], True, color.WHITE), self.font.render(player[1], True, color.WHITE)]
        self.turn     = 0

        self.clock    = pygame.time.Clock()
        self.v_y      = 0
        self.d_y      = 0
        self.clock.tick()
    
    def switch(self):
        print('switched!')
        if self.turn == 0:
            self.v_y = 3.5
        else:
            self.v_y = -3.5
        self.turn = 1 - self.turn

    def draw_on(self, x, y):

        self.clock.tick()
        # print(self.clock.get_time())
        if self.clock.get_time() >= 1:
            self.d_y += self.v_y
        
        if (self.d_y <= 0 or self.d_y >= 35):
            self.v_y = 0

        print(self.d_y)

        pygame.draw.rect(self.screen, (self.bg_color), (x, y, 200, 105))

        self.screen.blit(self.player[0], (x, y + self.d_y))
        self.screen.blit(self.player[1], (x, y + 35 + self.d_y))
        # self.screen.blit(self.player[1], (x, y + 70 + self.d_y))

        # không đổi
        pygame.draw.rect(self.screen, self.bg_color, (x, y, 220, 35))
        pygame.draw.rect(self.screen, self.bg_color, (x, y + 70, 220, 35))
        # pygame.draw.rect(self.screen, color.BLACK, (x, y, 200, 35))
        # pygame.draw.rect(self.screen, color.BLACK, (x, y + 70, 200, 35))

        self.screen.blit(pygame.font.SysFont('Consolas', 25).render('Play Turn:', True, color.WHITE), (x, y))
        delta = 5
        pygame.draw.rect(self.screen, color.BLACK, (x - delta, y - delta + 35, 220, 35 + delta * 2), 5, 10)
        
