import random

import source.s_level as s_level
import source.enemy_deploy as deploy


class Level14(s_level.MakeItRainLevel):
    def __init__(self, *pack):
        super().__init__(*pack)

        # colors = 'g'
        # enemies =
        # deploy.enemy_grid_deploy(cols=12, rows=2, colors=colors, initial_y=60, initial_x=0, x_speed=1, y_speed=1)

        # colors = 'r_bouncy'
        # enemies = deploy.enemy_grid_deploy(cols=1, rows=1, colors=colors, initial_y=60, initial_x=50, x_speed=0,
        #                                    y_speed=1)

        colors = 'b_split_bouncy_raining'
        enemies = [
            deploy.enemy_grid_deploy(cols=7, rows=3, colors=colors, initial_y=60, initial_x=60, x_speed=0,
                                     y_speed=1),
            deploy.enemy_grid_deploy(cols=7, rows=3, colors='r', initial_y=60, initial_x=500, x_speed=2,
                                     y_speed=0)
        ]
        for enemy_ in enemies:
            for enemy_row in enemy_.enemy_packs:
                for enemy_col in enemy_row:
                    enemy_col.hp = enemy_col.max_hp = 500

        enemies[0].enemy_y_lower_constraint = 50
        enemies[0].enemy_y_upper_constraint = 200
        enemies[0].enemy_y_speed_countdown = 0
        enemies[0].enemy_shoot_cooldown = self.raining_countdown - 70

        enemies[1].enemy_y_lower_constraint = 50
        enemies[1].enemy_y_upper_constraint = 200
        enemies[1].enemy_y_speed_countdown = 0
        enemies[1].enemy_shoot_cooldown = self.raining_countdown

        self.append_enemy(enemies)

        self.make_it_rain_idx = [0, 1]
        self.laser_speed = -19
        self.laser_countdown = 1000000
        self.laser_type = 3
        self.laser_dmg = 75
        self.laser_speed_score += 600
        self.extra_enemy_health = 200
        self.extra_enemy_bonus = 200
        self.min_space_between = 200
        self.max_space_between = self.min_space_between + 200

        self.max_waves = 1

        self.start_raining = 3000

        self.blocks.clear()
        self.make_blocks(random.choice(random.choice(self.enemies[0].enemy_packs)).sp.sprite.rect.centerx,
                         self.screen_height - 120, self.block_size, self.raining_shield, 'light blue')
        # self.make_multiple_blocks(max_space_between=self.max_space_between, min_space_between=self.min_space_between,
        #                           block_size=self.block_size * 1.3, shape=self.raining_shield, color='light blue')

        # enemies = \
        #     deploy.enemy_row_deploy(cols=12, colors='r',
        #                             initial_y=0, initial_x=900, x_speed=1, y_speed=0)
        # enemies.enemy_laser_speed = 18
        # enemies.enemy_shoot_cooldown = 10
        # for enemy_row in enemies.enemy_packs:
        #     for enemy_col in enemy_row:
        #         enemy_col.hp = enemy_col.max_hp = 5000
        #         enemy_col.dmg = 10
        # self.append_enemy(enemies)

    def special(self):
        # dif = self.current_timing - self.spawn_timer

        # rain_dif = self.current_timing - self.start_raining

        # timer
        # if dif < 8000 and self.enemies[len(self.enemies)-1].enemy_amount == 0:
        #     self.end_level = True

        # print(f'dif={dif}')

        # if self.enemies[0].enemy_amount != 0 and self.raining_times_counter <= self.raining_times:
        #     if self.start_raining <= rain_dif <= self.start_raining + self.space_time:
        #         if not self.is_rained:
        #             self.enemies[self.spawned_waves - 1].enemy_shoot_cooldown = 100000
        #             self.enemies[self.spawned_waves - 1].enemy_x_speed = 1
        #             self.enemies[self.spawned_waves - 1].enemy_y_speed = 0
        #             self.laser_countdown = 700 - self.enemies[0].enemy_amount * 10
        #             print('rain stopped')
        #             self.is_rained = True
        #     else:
        #         if self.is_rained:
        #             self.enemies[self.spawned_waves - 1].enemy_shoot_cooldown = self.raining_countdown
        #             self.enemies[self.spawned_waves - 1].enemy_x_speed = 0
        #             self.enemies[self.spawned_waves - 1].enemy_y_speed = 1
        #
        #             self.blocks.clear()
        #             self.max_space_between += self.enemies[0].enemy_amount * 2
        #             self.min_space_between += self.enemies[0].enemy_amount * 2
        #             self.make_multiple_blocks(max_space_between=self.max_space_between,
        #                                       min_space_between=self.min_space_between,
        #                                       block_size=self.block_size * 1.3, shape=self.raining_shield,
        #                                       color='light blue')
        #
        #             self.raining_times_counter += 1
        #             self.start_raining += self.space_time
        #             self.is_rained = False
        #             print('is raining')
        #             self.laser_countdown = 1000000
        #
        # else:
        #     self.laser_countdown = 100

        # if 2000 <= dif <= 4000 and self.spawned_waves == 1:
        #     self.enemies[self.spawned_waves - 1].enemy_shoot_cooldown = 100000
        #     self.enemies[self.spawned_waves - 1].enemy_x_speed = 1
        #
        # elif dif >= 4000 and self.spawned_waves == 1:
        #     self.enemies[self.spawned_waves - 1].enemy_shoot_cooldown = 100
        #     self.enemies[self.spawned_waves - 1].enemy_x_speed = 0

        # self.moving_blocks()

        super().special()

    def is_not_raining(self):
        for idx in self.make_it_rain_idx:
            self.enemies[idx].enemy_x_speed = random.choice([1, -1])
            self.enemies[idx].enemy_y_speed = 0
        self.laser_countdown = 650 - self.enemies[0].enemy_amount * 10

    def is_raining(self):
        for idx in self.make_it_rain_idx:
            self.enemies[idx].enemy_x_speed = 0
            self.enemies[idx].enemy_y_speed = 1

    def done_raining(self):
        self.laser_countdown = 100
        for idx in self.make_it_rain_idx:
            self.enemies[idx].enemy_shoot_cooldown = 500
