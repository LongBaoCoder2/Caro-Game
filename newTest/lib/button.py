import pygame, random

class Button:

    # khởi tạo
    def __init__(self, image, x, y, dx = 0, dy = 0, dw = 0, dh = 0):
        self.dx = dx
        self.dy = dy
        self.dw = dh
        self.dh = dh
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    # vẽ button lên một surface
    def draw_on(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # kiểm tra sai số bằng đường vẽ hình chữ nhật màu đỏ
        # pygame.draw.rect(screen, color.RED, (self.rect.x + 50, self.rect.y + 50, self.image.get_width() - 100, self.image.get_height() - 100), 1)
    
    # cập nhật hình ảnh
    def update_image(self, image):
        self.image = image

    # kiểm tra hovered với sai số
    def is_hovered(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        (x, y, width, height) = (self.rect.x + self.dx, self.rect.y + self.dy, self.image.get_width() - self.dw, self.image.get_height() - self.dh)
        if (mouse_x >= x and mouse_x <= x + width and mouse_y >= y and mouse_y <= y + height):
            # print('hovered', random.random())
            return True
        return False
    
    # kiểm tra clicked với sai số
    def is_clicked(self):
        if self.is_hovered() and pygame.mouse.get_pressed()[0] == 1:
            print('clicked', random.random())
            return True
        return False
