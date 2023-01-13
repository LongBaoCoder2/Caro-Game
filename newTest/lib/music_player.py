import pygame 

class MusicPlayer:
    def __init__(self):
        self.ingame_sound_path='res/musicgame/musicgame1.mp3'
        self.win_sound_path='res/winmusic/win.mp3'
        self.click_sound_path='res/clickmusic/click.mp3'
        self.menu_path='res/musicgame/musicgame2.mp3'
        self.ingame_sound = pygame.mixer.Sound( self.ingame_sound_path )
        self.win_sound = pygame.mixer.Sound(  self.win_sound_path )
        self.click_sound = pygame.mixer.Sound( self.click_sound_path )
        self.menu_sound = pygame.mixer.Sound( self.menu_path )
        self.ingame_sound_channel = pygame.mixer.Channel(0)
        self.win_channel = pygame.mixer.Channel(1)
        self.click_channel = pygame.mixer.Channel(2)
        self.menu_channel = pygame.mixer.Channel(3)
    def ingame_sound_play(self):
        self.ingame_sound_channel.play(self.ingame_sound, loops=-1, fade_ms=1000)
    def ingame_sound_pause(self):
        self.ingame_sound_channel.fadeout(500)

    def win_play(self):
        self.win_channel.play(self.win_sound, loops=0, maxtime=3000, fade_ms=500)
    def click_play(self):
        self.click_channel.play(self.click_sound, loops=0)
    def menu_play(self):
        self.menu_channel.play(self.menu_sound, fade_ms=1000)
    def menu_pause (self):
        self.menu_channel.fadeout(500)