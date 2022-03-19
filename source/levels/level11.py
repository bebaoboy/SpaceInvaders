import pygame

import source.level as level
import source.enemy_deploy as deploy


class Level11(level.Level):
    def __init__(self, *pack):
        super().__init__(*pack)

        self.intro = 'gatling madness'

        colors = [
            ['p_gatling'] * 5,
            ['b', 'p_gatling', 'b', 'p_gatling', 'b'],
            ['g'] * 5,
            ['p_gatling'] * 5,
            ['p_gatling'] * 5
        ]
        enemies = deploy.enemy_grid_deploy(cols=5, rows=5, colors=colors, initial_y=60, initial_x=200, x_speed=1,
                                           y_speed=1)
        enemies.enemy_y_lower_constraint = 50
        enemies.enemy_y_upper_constraint = 200

        enemies.enemy_shoot_cooldown = 1000
        for enemy_row in enemies.enemy_packs:
            for enemy_col in enemy_row:
                enemy_col.max_hp = enemy_col.hp = 175
                enemy_col.dmg = 20
        self.append_enemy(enemies)

        self.laser_type = 5
        self.laser_countdown = 700

        self.max_waves = 6

    def special(self):
        dif = self.current_timing - self.spawn_timer
        # print(self.current_timing - self.spawn_timer)

        if dif >= 4000 and self.spawned_waves == 1:
            self.spawn_timer = self.current_timing
            colors = 'p_gatling'
            enemies = \
                deploy.enemy_grid_deploy(rows=3, cols=7, colors=colors, initial_y=50, x_speed=2, y_speed=0)
            enemies.enemy_y_speed_countdown = 0
            enemies.enemy_y_speed_drop_time = 0
            self.append_enemy(enemies)

        elif dif >= 7000 and self.spawned_waves == 2:
            enemy1 = \
                deploy.enemy_col_deploy(rows=2, colors='p_gatling', initial_y=0, initial_x=20, x_speed=1, y_speed=1)
            enemy1.enemy_y_speed_countdown = 1000
            enemy1.enemy_y_speed_drop_time = 3
            enemy2 = \
                deploy.enemy_col_deploy(rows=2, colors='p_gatling',
                                        initial_y=0, initial_x=self.screen_width - 50, x_speed=-1, y_speed=1)
            enemy2.enemy_y_speed_countdown = 1000
            enemy2.enemy_y_speed_drop_time = 3
            self.append_enemy(enemy1)
            self.append_enemy(enemy2)

        elif dif >= 10000 and self.spawned_waves == 4:
            enemies = \
                deploy.enemy_row_deploy(cols=5, colors='p_gatling',
                                        initial_y=0, initial_x=20, x_speed=2, y_speed=2, col_distance=100)
            enemies.enemy_y_speed_countdown = 0
            enemies.enemy_y_speed_drop_time = 0
            self.append_enemy(enemies)

        elif dif >= 12000 and self.spawned_waves == 5:
            enemies = \
                deploy.enemy_row_deploy(cols=5, colors='p_gatling',
                                        initial_y=0, initial_x=self.screen_width / 2, x_speed=0, y_speed=2,
                                        col_distance=100)
            enemies.enemy_y_speed_countdown = 0
            enemies.enemy_y_speed_drop_time = 0
            enemies2 = \
                deploy.enemy_row_deploy(cols=5, colors='p_gatling',
                                        initial_y=self.screen_height, initial_x=self.screen_width / 2, x_speed=0, y_speed=-1,
                                        col_distance=100)
            enemies2.enemy_y_speed_countdown = 0
            enemies2.enemy_y_speed_drop_time = 0
            self.append_enemy([enemies, enemies2])
