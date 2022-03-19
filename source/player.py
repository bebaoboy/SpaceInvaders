import pygame

from source.resource_path import resource_path


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, color=None):
        super().__init__()
        self.image = pygame.image.load(resource_path('graphics/player.png')).convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)

        self.max_x_constraint = constraint

    def update(self, pos):
        self.rect.centerx = pos
        if self.rect.x > self.max_x_constraint - self.rect.width / 2:
            self.rect.x = self.max_x_constraint - self.rect.width / 2
