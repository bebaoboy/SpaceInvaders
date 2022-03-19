import random

import pygame
import source.collectibles as collectibles
import source.enemy_deploy as deploy


class GifBackground:
    def __init__(self, screen, width, height):
        self.screen_width = width
        self.screen_height = height
        self.screen = screen

        # self.coin = collectibles.Coin(random.randint(0, self.screen_width), 0, self.screen_width,
        #                               self.screen_height - 100,
        #                               random.randint(1, 4), time_to_live=10000)
        # self.coins = pygame.sprite.Group()
        self.timer = pygame.time.get_ticks()
        self.falling_objects = {
            'coin': pygame.sprite.Group(),
            'health_bag': pygame.sprite.Group(),
        }
        self.enemies = []

        self.choice = ['coin'] * 9 + ['health_bag'] * 2 + ['enemy'] * 4

    def draw(self):
        # self.coins.draw(self.screen)
        for name, obj in self.falling_objects.items():
            obj.draw(self.screen)
        for enemies in self.enemies:
            for enemy_row in enemies.enemy_packs:
                for enemy_col in enemy_row:
                    if enemy_col is not None:
                        if enemy_col.another_img is not None:
                            self.screen.blit(enemy_col.another_img, enemy_col.another_rect)
                        else:
                            enemy_col.sp.draw(self.screen)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.timer >= 550:
            choice = random.choice(self.choice)
            if choice == 'coin':
                size = random.randint(10, 30)
                c = collectibles.Coin(random.randint(-10, self.screen_width + 10), random.randint(-20, 0),
                                      self.screen_width,
                                      self.screen_height + 100,
                                      random.randint(1, 3), size_x=size, size_y=size, time_to_live=17000)
                c.image.set_alpha(random.choice([128, 190, 255]))
                self.falling_objects[choice].add(c)
            elif choice == 'health_bag':
                size = random.randint(30, 40)
                h = collectibles.HealthBag(
                    random.randint(-10, self.screen_width + 10), random.randint(-20, 0),
                    self.screen_width,
                    self.screen_height + 100,
                    0, random.randint(1, 3), size_x=size, size_y=size
                )
                h.image.set_alpha(random.choice([128, 190, 255]))
                self.falling_objects[choice].add(h)
            elif choice == 'enemy':
                size = random.randint(10, 50)
                x = random.randint(-10, self.screen_width + 10)
                y = random.randint(-20, 0)
                enemies = deploy.enemy_col_deploy(rows=1,
                                                  initial_x=x,
                                                  initial_y=y,
                                                  y_speed=random.randint(2, 3),
                                                  colors=random.choice([_ for _ in deploy.enemy_stat]))
                enemies.enemy_y_speed_countdown = 0
                enemies.enemy_y_speed_drop_time = 0
                enemies.enemy_packs[0][0].sp.sprite.image = \
                    pygame.transform.scale(enemies.enemy_packs[0][0].sp.sprite.image, (size + 5, size + 5))
                enemies.enemy_packs[0][0].sp.sprite.rect = \
                    enemies.enemy_packs[0][0].sp.sprite.image.get_rect(topleft=(x, y))
                enemies.enemy_packs[0][0].ani = None
                enemies.enemy_packs[0][0].rotate_angle = random.randint(-180, 180)
                enemies.enemy_packs[0][0].rotate_speed = random.randint(2, 5)
                enemies.enemy_packs[0][0].rotate_countdown = random.randint(0, 1)
                enemies.enemy_packs[0][0].mlee_timer = pygame.time.get_ticks()
                enemies.enemy_packs[0][0].sp.sprite.image.set_alpha(random.choice([128, 190, 255]))
                self.enemies.append(enemies)

            self.timer = current_time
        for name, obj in self.falling_objects.items():
            obj.update()
        for enemies in self.enemies:
            for enemy_row in enemies.enemy_packs:
                for enemy_col in enemy_row:
                    if enemy_col is not None:
                        if current_time - enemy_col.mlee_timer >= 15000:
                            enemy_row.pop()
                        else:
                            enemy_col.update(current_time, 0, enemies.enemy_y_speed)
