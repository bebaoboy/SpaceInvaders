import pygame

from source.resource_path import resource_path


class SoundController:
    def __init__(self):
        self.sound_dict = {
            'laser': pygame.mixer.Sound(resource_path('audio/laser.wav')),
            'hit': pygame.mixer.Sound(resource_path('audio/hit.wav')),
            'block': pygame.mixer.Sound(resource_path('audio/block.wav')),
            'extra_hit': pygame.mixer.Sound(resource_path('audio/extra.wav')),
            'enemy_explosion': pygame.mixer.Sound(resource_path('audio/explosion.wav')),
            'coin_hit': pygame.mixer.Sound(resource_path('audio/coin.wav'))
        }
        self.unmute_sound()

        self.music_dict = {
            'main_theme': resource_path('music/main_theme.ogg'),
            'world_1': resource_path('music/world_1.ogg'),
            'endless': resource_path('music/endless.ogg')
        }
        self.is_muted = False
        self.currently_playing = ''

    def play_music(self, level_num=-1):
        if level_num == -1:
            self.play('main_theme')
        elif 0 <= level_num <= 10:
            self.play('world_1')
        else:
            self.play('endless')

    def play(self, s):
        if s == self.currently_playing:
            return
        pygame.mixer.music.load(self.music_dict[s])
        self.currently_playing = s
        if not self.is_muted:
            self.unmute_music()
        pygame.mixer.music.play(loops=-1)

    def mute_music(self):
        pygame.mixer.music.set_volume(0.0)
        self.is_muted = True

    def unmute_music(self):
        pygame.mixer.music.set_volume(0.2)

    def play_sound(self, s):
        if s in self.sound_dict:
            self.sound_dict[s].play()

    def unmute_sound(self):
        self.sound_dict['laser'].set_volume(0.12)
        self.sound_dict['hit'].set_volume(0.2)
        self.sound_dict['block'].set_volume(0.15)
        self.sound_dict['extra_hit'].set_volume(0.2)
        self.sound_dict['enemy_explosion'].set_volume(0.2)
        self.sound_dict['coin_hit'].set_volume(0.15)

    def mute_sound(self):
        for name, sound in self.sound_dict.items():
            sound.set_volume(0)
