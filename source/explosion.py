import pygame.time
from pygame import sprite, transform, time
import source.resource_manager as resource_manager


class EnemyExplosion(sprite.Sprite):
    def __init__(self, current_time, colors: str, x, y, enemy_width, enemy_height):
        super().__init__()
        self.color = colors.split('_')[0]
        self.enemy_width = enemy_width
        self.enemy_height = enemy_height
        self.image = resource_manager.explosion_pic[self.color]
        self.image2 = self.image
        self.image3 = self.image2
        self.ratio = self.enemy_width / (self.image.get_width() * 1.2)
        if self.ratio != 1:
            self.ratio *= 3
        self.image = transform.scale(
            self.image, (self.enemy_width, self.enemy_height))
        self.image2 = transform.scale(
            self.image2, (self.enemy_width * 1.17, self.enemy_height * 1.17))
        self.image3 = transform.scale(
            self.image3, (self.enemy_width * 1.25, self.enemy_height * 1.25))
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = current_time

    def update(self, current_timing, screen: pygame.surface.Surface):
        passed = current_timing - self.timer
        if passed <= 100:
            screen.blit(self.image, self.rect)
        elif passed <= 175:
            # game.screen.blit(self.image2, (self.rect.x - 6, self.rect.y - 6))
            self.image2.set_alpha(240)
            screen.blit(self.image2, (self.rect.x - 0.5, self.rect.y - 0.5))
        elif passed <= 225 * self.ratio:
            # game.screen.blit(self.image2, (self.rect.x - 6, self.rect.y - 6))
            self.image3.set_alpha(128)
            screen.blit(self.image3, (self.rect.x - 2, self.rect.y - 2))
        elif passed <= 300 * self.ratio:
            # game.screen.blit(self.image2, (self.rect.x - 6, self.rect.y - 6))
            self.image3.set_alpha(100)
            screen.blit(self.image3, (self.rect.x - 2, self.rect.y - 2))
        elif 500 * self.ratio < passed:
            self.kill()
