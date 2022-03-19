import random

import pygame.time
import source.level as level
import source.enemy_deploy as deploy


class Level4(level.Level):
    def __init__(self, *pack):
        super().__init__(*pack)
        self.intro = 'CLASSIC INVASION #2'
        # colors = [
        #     ['r'] * 7,
        #     [''] + ['r'] * 5 + [''],
        #     [''] * 2 + ['r'] * 3 + [''] * 2,
        #     [''] * 3 + ['r'] + [''] * 3
        # ]
        # enemies = \
        #     deploy.enemy_grid_deploy(rows=4, cols=7, colors=colors, initial_y=100)
        # self.append_enemy(enemies)

        self.player_health = max (self.player_health + 1000, self.player_max_health)

        self.laser_type = 4
        self.laser_speed = -15
        self.laser_countdown = 500
        self.laser_dmg = 70
        self.equipment_type = 3

        self.max_waves = 7

        self.max_space_between = 600
        self.max_space_between = 400
        self.blocks.clear()
        self.make_multiple_blocks(max_space_between=self.max_space_between, min_space_between=self.min_space_between)

    def special(self):
        dif = self.current_timing - self.spawn_timer
        # print(self.current_timing - self.spawn_timer)
        space_time = 5000

        if (dif >= space_time or self.spawned_waves == 0) and self.spawned_waves < self.max_waves:
            self.spawn_timer = self.current_timing
            choice = random.randint(1, 2)
            colors = [
                ['r'] * 7,
                [''] + ['y'] * 5 + [''],
                [''] * 2 + ['g'] * 3 + [''] * 2,
                [''] * 3 + ['b'] + [''] * 3
            ]
            if choice == 1:
                enemies = \
                    deploy.enemy_grid_deploy(rows=4, cols=7, colors=colors,
                                             initial_y=0, initial_x=self.screen_width - 50,
                                             x_speed=-1, y_speed=1, col_distance=60)
            else:
                enemies = \
                    deploy.enemy_grid_deploy(rows=4, cols=7, colors=colors,
                                             initial_y=0, initial_x=20, x_speed=1, y_speed=1, col_distance=60)

            enemies.enemy_y_speed_countdown = 10
            self.append_enemy(enemies)
