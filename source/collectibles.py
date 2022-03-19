import random

import pygame
import source.spritesheet as spritesheet
from source.resource_path import resource_path
import source.resource_manager as resource_manager


class Collectibles(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed_y, speed_x=0, size_x=30, size_y=30):
        super().__init__()

        self.pos_x = x
        self.pos_y = y
        self.image: pygame.surface.Surface
        self.rect: pygame.rect.Rect

        self.size_x = size_x
        self.size_y = size_y
        self.screen_width = width
        self.screen_height = height
        self.speed_x = speed_x
        self.speed_y = speed_y

        self.time_to_live = 5000
        self.timer = pygame.time.get_ticks()
        self.current_timing = 0

    def update(self):
        self.current_timing = pygame.time.get_ticks()
        if self.current_timing - self.timer >= self.time_to_live != -1:
            self.kill()
            return
        if self.rect.bottom < self.screen_height:
            self.rect.centery += self.speed_y


class HealthBag(Collectibles):
    def __init__(self, x, y, width, height, hp, speed_y=3, speed_x=0, size_x=40, size_y=40):
        super().__init__(x, y, width, height, speed_y, speed_x, size_x, size_y)

        self.image = resource_manager.collectibles_pic['health_bag']
        self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)

        self.hp = hp
        self.time_to_live = 6000


class Coin(Collectibles):
    def __init__(self, x, y, width, height, speed_y, speed_x=0, size_x=30, size_y=30, ani_time=200, time_to_live=22000):
        super().__init__(x, y, width, height, speed_y, speed_x, size_x, size_y)

        # self.height_y_upper_constraint = constraint_y_up
        # self.height_y_lower_constraint = constraint_y_down
        # self.width_x_left_constraint = constraint_x_left
        # self.width_x_right_constraint = constraint_x_right

        self.sprites = []
        self.sheets = resource_manager.collectibles_pic['coin']
        for i in range(0, 6):
            img = self.sheets.image_at((i * 83, 0, 83, 83), colorkey=(0, 0, 0))
            img = pygame.transform.scale(img, (self.size_x, self.size_y))
            self.sprites.append(img)

        self.current_frame = 0
        self.image = self.sprites[self.current_frame]

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)

        self.ani_time = random.randint(ani_time - 50, ani_time + 100)
        self.change_frame = False
        self.ani_timer = pygame.time.get_ticks()

        self.time_to_live = time_to_live

    def animate(self):
        self.current_timing = pygame.time.get_ticks()
        if self.current_timing - self.ani_timer >= self.ani_time:
            # print('ani')
            self.change_frame = True
            self.ani_timer = self.current_timing

    def update(self):
        super().update()

        self.animate()
        if self.change_frame:
            self.current_frame = (self.current_frame + 1) % len(self.sprites)
            self.change_frame = False
            self.image = self.sprites[self.current_frame]
