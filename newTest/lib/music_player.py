import pygame 

class MusicPlayer:
    def __init__(self, background_sound, win_sound, click_sound, menu_sound):
        self.background_sound = pygame.mixer.Sound( background_sound )
        self.win_sound = pygame.mixer.Sound( win_sound )
        self.click_sound = pygame.mixer.Sound( click_sound )
        self.menu_soud = pygame.mixer.Sound( menu_sound )
        self.bgsound_channel = pygame.mixer.Channel(0)
        self.win_channel = pygame.mixer.Channel(1)
        self.click_channel = pygame.mixer.Channel(2)
        self.menu_channel = pygame.mixer.Channel(3)
    def bgsound_play(self):
        self.bgsound_channel.play(self.background_sound, fade_ms=1000)
    def bgsound_pause(self ):
        self.bgsound_channel.fadeout(600)

    def win_play(self):
        self.win_channel.play(self.win_sound, loops=0, maxtime=3000, fade_ms=500)
    def click_play(self):
        self.click_channel.play(self.click_sound, loops=0)
    def menu_play(self):
        self.menu_channel.play(self.menu_soud, fade_ms=1000)
    def menu_pause (self):
        self.menu_channel.fadeout(1000)