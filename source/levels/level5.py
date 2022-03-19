import random

import pygame.time
import source.s_level as s_level
import source.enemy_deploy as deploy


class Level5(s_level.BossLevel):
    def __init__(self, *pack):
        super().__init__(*pack)

        colors = 'y_boss'
        enemies = \
            deploy.enemy_col_deploy(rows=1, colors=colors, initial_y=-100, initial_x=200)
        enemies_sprite = enemies.enemy_packs[0][0].sp.sprite
        enemies.enemy_shoot_cooldown = 10
        enemies_sprite.image = pygame.transform.scale(
            enemies_sprite.image, (enemies_sprite.image.get_rect().width * 10,
                                   enemies_sprite.image.get_rect().height * 10))
        enemies.enemy_packs[0][0].sp.sprite.rect = \
            enemies.enemy_packs[0][0].sp.sprite.image.get_rect(topleft=(200, -100))

        self.append_enemy(enemies)

        self.laser_type = 6
        self.laser_speed = -14
        self.laser_countdown = 650
        self.laser_dmg = 65
        self.equipment_type = 3

        self.max_waves = 12

        self.max_space_between = 600
        self.max_space_between = 400

        self.player_health = self.player_max_health

        self.extra_enemy_spawn_min_time = 5000
        self.extra_enemy_spawn_max_time = 7000
        self.extra_enemy_spawn_time = 1000

    def special(self):
        dif = self.current_timing - self.spawn_timer
        space_time = 7000
        # print(self.current_timing - self.spawn_timer)
        if self.enemies[0].enemy_amount == 0:
            self.end_level = True

        if dif >= space_time and self.spawned_waves <= 10:
            self.spawn_timer = self.current_timing
            choice = random.randint(0, 1)
            if choice == 0:
                enemies = \
                    deploy.enemy_row_deploy(cols=random.randint(4, 7), colors='y',
                                            initial_y=0, initial_x=20, x_speed=2, y_speed=2, col_distance=100)
            else:
                enemies = \
                    deploy.enemy_row_deploy(cols=random.randint(4, 7), colors='y',
                                            initial_y=0, initial_x=self.screen_width - 50, x_speed=-2, y_speed=2,
                                            col_distance=100)

            enemies.enemy_y_speed_countdown = 0
            enemies.enemy_y_speed_drop_time = 0
            self.append_enemy(enemies)

        elif dif >= 5000 and self.spawned_waves == 11 and self.enemies[0].enemy_amount != 0:
            self.make_multiple_blocks()
            self.laser_speed = -8
            enemies = \
                deploy.enemy_row_deploy(cols=12, colors='r',
                                        initial_y=0, initial_x=0, x_speed=0.5, y_speed=0)
            enemies.enemy_laser_speed = 15
            enemies.enemy_shoot_cooldown = 50
            for enemy_row in enemies.enemy_packs:
                for enemy_col in enemy_row:
                    enemy_col.hp = enemy_col.max_hp = 2000
                    enemy_col.dmg = 30
            self.append_enemy(enemies)

    def recover(self):
        if self.enemies[0].enemy_packs[0][0] is not None:
            self.enemies[0].enemy_packs[0][0].sp.sprite.image = pygame.transform.scale(
                self.enemies[0].enemy_packs[0][0].sp.sprite.image, (
                    self.enemies[0].enemy_packs[0][0].sp.sprite.image.get_rect().width * 10,
                    self.enemies[0].enemy_packs[0][0].sp.sprite.image.get_rect().height * 10))
            self.enemies[0].enemy_packs[0][0].sp.sprite.rect = \
                self.enemies[0].enemy_packs[0][0].sp.sprite.image.get_rect(topleft=(200, -100))
