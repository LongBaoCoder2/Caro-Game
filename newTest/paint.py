class PAINT:
    def __init__(self, screen):
        self.screen = screen

    def get_font(self, size):
        return pygame.font.SysFont('Helvetica', size)

    def render_surface(self, Surface, topleft):
        self.screen.blit(Surface, topleft)
