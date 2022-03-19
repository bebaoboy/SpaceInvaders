import random

import pygame.time
import source.s_level as s_level
import source.enemy_deploy as deploy


class Level10(s_level.BossLevel):
    def __init__(self, *pack):
        super().__init__(*pack)

        colors = 'b_boss_rotate'
        enemies = \
            deploy.enemy_col_deploy(rows=1, colors=colors, initial_y=100, initial_x=200, x_speed=7, y_speed=1)
        enemies_sprite = enemies.enemy_packs[0][0].sp.sprite
        enemies.enemy_shoot_cooldown = 1000
        enemies_sprite.image = pygame.transform.scale(
            enemies_sprite.image, (enemies_sprite.image.get_rect().width * 8,
                                   enemies_sprite.image.get_rect().height * 8))

        enemies.enemy_packs[0][0].ani = None
        #
        # enemies.enemy_packs[0][0].normal_ani = enemies_sprite.image
        #
        # enemies.enemy_packs[0][0].ani = pygame.transform.scale(
        #     enemies.enemy_packs[0][0].ani,
        #     (enemies.enemy_packs[0][0].ani.get_rect().width * 10,
        #      enemies.enemy_packs[0][0].ani.get_rect().height * 10))

        enemies.enemy_packs[0][0].sp.sprite.rect = \
            enemies.enemy_packs[0][0].sp.sprite.image.get_rect(topleft=(200, 100))

        enemies.enemy_packs[0][0].rotate_speed = 30
        enemies.enemy_packs[0][0].rotate_countdown = 6
        enemies.enemy_y_speed_countdown = 0
        enemies.enemy_y_speed_drop_time = 0
        enemies.enemy_y_speed_drop_rate = 5
        enemies.enemy_x_left_constraint = 200
        enemies.enemy_x_right_constraint = self.screen_width - 200
        enemies.enemy_y_lower_constraint = -50
        enemies.enemy_y_upper_constraint = self.screen_height / 2 - 160

        self.append_enemy(enemies)

        self.laser_type = 5
        self.laser_speed = -13
        self.laser_countdown = 600
        self.laser_dmg = 750
        self.equipment_type = 3

        self.max_waves = 11

        self.max_space_between = 600
        self.min_space_between = 400
        self.blocks.clear()
        self.make_multiple_blocks(max_space_between=self.max_space_between, min_space_between=self.min_space_between)

        self.player_health = self.player_max_health

        self.extra_enemy_spawn_min_time = 3500
        self.extra_enemy_spawn_max_time = 7000
        self.extra_enemy_spawn_time = 1000
        self.extra_enemy_bonus = 500

        self.rot_timer = 0
        self.max_speed = 14 + 1
        self.speed = 5

    def special(self):
        dif = self.current_timing - self.spawn_timer
        space_time = 7000
        rot_time = 8000
        # print(self.current_timing - self.spawn_timer)
        if self.enemies[0].enemy_amount == 0:
            self.spawned_waves = self.max_waves
            return

        if dif >= space_time:
            self.spawn_timer = self.current_timing
            choice = random.randint(0, 3)
            cl = random.choice(['r', 'y', 'g'])
            if choice == 0:
                enemies = \
                    deploy.enemy_row_deploy(cols=random.randint(4, 7), colors=cl,
                                            initial_y=0, initial_x=20, x_speed=2, y_speed=2, col_distance=100)
            elif choice == 1:
                enemies = \
                    deploy.enemy_row_deploy(cols=random.randint(4, 7), colors=cl,
                                            initial_y=0, initial_x=self.screen_width - 50, x_speed=-2, y_speed=2,
                                            col_distance=100)
            elif choice == 2:
                enemies = \
                    deploy.enemy_col_deploy(rows=random.randint(3, 5), colors=cl,
                                            initial_y=0, initial_x=self.screen_width - 50, x_speed=-2, y_speed=2)
            else:
                enemies = \
                    deploy.enemy_col_deploy(rows=random.randint(3, 5), colors=cl,
                                            initial_y=0, initial_x=20, x_speed=2, y_speed=2)

            enemies.enemy_y_speed_countdown = 0
            enemies.enemy_y_speed_drop_time = 0

            self.append_enemy(enemies)

        dif = self.current_timing - self.rot_timer

        if rot_time - 3500 <= dif < rot_time and 0 <= dif % 100 <= 55:
            if self.enemies[0].enemy_x_speed > 0:
                dx = max(self.enemies[0].enemy_x_speed - .1, 1)
            else:
                dx = min(self.enemies[0].enemy_x_speed + .1, -1)
            if self.enemies[0].enemy_y_speed > 0:
                dy = max(self.enemies[0].enemy_y_speed - .1, 1)
            else:
                dy = min(self.enemies[0].enemy_y_speed + .1, -1)
            self.enemies[0].enemy_y_speed = dy
            self.enemies[0].enemy_x_speed = dx
            axe = self.enemies[0].enemy_packs[0][0].rotate_speed
            if axe > 0:
                self.enemies[0].enemy_packs[0][0].rotate_speed = max(axe - .6 * (axe / 180), 3)
            else:
                self.enemies[0].enemy_packs[0][0].rotate_speed = min(axe + .6 * (abs(axe) / 180), 3)
            print(f'SLOWWWWWWWWWW{self.enemies[0].enemy_packs[0][0].rotate_speed},x={dx},y={dy}')

        elif dif >= rot_time:
            print('changeeeeeeeeeeeeeeee')
            self.rot_timer = self.current_timing
            self.enemies[0].enemy_packs[0][0].rotate_speed = random.choice([-60, -45, -30, -10, 10, 30, 60])
            self.enemies[0].enemy_packs[0][0].rotate_countdown = random.randint(6, 10)
            self.speed = max(self.speed + .35, self.max_speed)
            speed = random.choice([_ for _ in range(5, int(self.speed))])
            neg = random.choice([0, 1])
            if neg:
                self.enemies[0].enemy_x_speed = -speed
            else:
                self.enemies[0].enemy_x_speed = speed
            speed = random.choice([_ for _ in range(2, 5)])
            neg = random.choice([0, 1])
            if neg:
                self.enemies[0].enemy_y_speed = -speed
            else:
                self.enemies[0].enemy_y_speed = speed
            self.enemies[0].enemy_shoot_cooldown = max(80, self.enemies[0].enemy_shoot_cooldown - 15)
            self.enemies[0].enemy_y_upper_constraint = min(self.enemies[0].enemy_y_upper_constraint + 50,
                                                           self.screen_height - 200)

        self.moving_blocks()
        # space_time = 70
        # # print(self.current_timing - self.spawn_timer)
        #
        # if dif >= space_time and self.spawned_waves <= 10:
        #     self.spawn_timer = self.current_timing
        #     for enemy_row in self.enemies[0].enemy_packs:
        #         for enemy_col in enemy_row:
        #             if enemy_col is not None:
        #                 if self.size is None:
        #                     self.size = enemy_col.sp.sprite.image.get_size()
        #                 print(enemy_col.sp.sprite.rect.center, enemy_col.sp.sprite.image.get_rect().center)

    def recover(self):
        if self.enemies[0].enemy_packs[0][0] is not None:
            self.enemies.enemy_packs[0][0].image = pygame.transform.scale(
                self.enemies.enemy_packs[0][0].image, (
                    self.enemies.enemy_packs[0][0].image.get_rect().width * 8,
                    self.enemies.enemy_packs[0][0].image.get_rect().height * 8))
            self.enemies.enemy_packs[0][0].sp.sprite.rect = \
                self.enemies.enemy_packs[0][0].sp.sprite.image.get_rect(topleft=(200, 100))
