import pygame

import source.level as level
import source.enemy_deploy as deploy


class Level8(level.Level):
    def __init__(self, *pack):
        super().__init__(*pack)

        self.intro = 'highway don"t care'
        colors = 'y'
        enemies = deploy.enemy_grid_deploy(cols=50, rows=1, col_distance=100,
                                           colors=colors, initial_y=20, initial_x=self.screen_width - 2, x_speed=-2,
                                           y_speed=0)

        enemies.enemy_shoot_cooldown = 50
        enemies.enemy_x_left_constraint = -5001
        enemies.enemy_x_right_constraint = self.screen_width + 5000
        for enemy_row in enemies.enemy_packs:
            for enemy_col in enemy_row:
                enemy_col.dmg = 20
        self.append_enemy(enemies)

        colors = 'r'
        enemies = deploy.enemy_grid_deploy(cols=50, rows=1, col_distance=100,
                                           colors=colors, initial_y=120, initial_x=-4900, x_speed=3,
                                           y_speed=0)

        enemies.enemy_shoot_cooldown = 50
        enemies.enemy_x_left_constraint = -5001
        enemies.enemy_x_right_constraint = self.screen_width + 5000
        for enemy_row in enemies.enemy_packs:
            for enemy_col in enemy_row:
                enemy_col.max_hp = enemy_col.hp = 275
                enemy_col.dmg = 20
        self.append_enemy(enemies)

        colors = 'g'
        enemies = deploy.enemy_grid_deploy(cols=50, rows=1, col_distance=100,
                                           colors=colors, initial_y=220, initial_x=self.screen_width - 2, x_speed=-1,
                                           y_speed=0)

        enemies.enemy_shoot_cooldown = 50
        enemies.enemy_x_left_constraint = -5001

        # minus width if wanted to come back: 5000 - self.screen_width - 1
        enemies.enemy_x_right_constraint = self.screen_width + 5000
        for enemy_row in enemies.enemy_packs:
            for enemy_col in enemy_row:
                enemy_col.dmg = 20
        self.append_enemy(enemies)

        colors = 'y'
        enemies = deploy.enemy_grid_deploy(cols=50, rows=1, col_distance=100,
                                           colors=colors, initial_y=420, initial_x=-4900, x_speed=2,
                                           y_speed=0)

        enemies.enemy_shoot_cooldown = 500
        enemies.enemy_x_left_constraint = -5001
        enemies.enemy_x_right_constraint = self.screen_width + 5000
        for enemy_row in enemies.enemy_packs:
            for enemy_col in enemy_row:
                enemy_col.max_hp = enemy_col.hp = 275
                enemy_col.dmg = 20
        self.append_enemy(enemies)

        colors = 'r'
        enemies = deploy.enemy_grid_deploy(cols=50, rows=1, col_distance=100,
                                           colors=colors, initial_y=520, initial_x=self.screen_width - 2, x_speed=-3,
                                           y_speed=0)

        enemies.enemy_shoot_cooldown = 50
        enemies.enemy_x_left_constraint = -5001

        # minus width if wanted to come back: 5000 - self.screen_width - 1
        enemies.enemy_x_right_constraint = self.screen_width + 5000
        for enemy_row in enemies.enemy_packs:
            for enemy_col in enemy_row:
                enemy_col.dmg = 20
        self.append_enemy(enemies)

        colors = 'b'
        enemies = deploy.enemy_grid_deploy(cols=50, rows=1, col_distance=100,
                                           colors=colors, initial_y=320, initial_x=-4900, x_speed=-4,
                                           y_speed=0)

        enemies.enemy_shoot_cooldown = 50
        enemies.enemy_x_left_constraint = -(5000 - self.screen_width - 1)

        # minus width if wanted to come back: 5000 - self.screen_width - 1
        enemies.enemy_x_right_constraint = 5000 - self.screen_width - 1
        for enemy_row in enemies.enemy_packs:
            for enemy_col in enemy_row:
                enemy_col.dmg = 20
        self.append_enemy(enemies)

        self.laser_type = 3
        self.laser_countdown = 500
        self.laser_speed_score -= 40
        self.laser_dmg = 60

        self.max_waves = 6

    def special(self):
        dif = self.current_timing - self.spawn_timer
        # print(self.current_timing - self.spawn_timer)

        # if dif >= 4000 and self.spawned_waves == 1:
        #     self.spawn_timer = self.current_timing
        #     colors = 'p_gatling'
        #     enemies = \
        #         deploy.enemy_grid_deploy(rows=3, cols=7, colors=colors, initial_y=50, x_speed=2, y_speed=0)
        #     enemies.enemy_y_speed_countdown = 0
        #     enemies.enemy_y_speed_drop_time = 0
        #     self.append_enemy(enemies)
        #
        # elif dif >= 7000 and self.spawned_waves == 2:
        #     enemy1 = \
        #         deploy.enemy_col_deploy(rows=2, colors='p_gatling', initial_y=0, initial_x=20, x_speed=1, y_speed=1)
        #     enemy1.enemy_y_speed_countdown = 1000
        #     enemy1.enemy_y_speed_drop_time = 3
        #     enemy2 = \
        #         deploy.enemy_col_deploy(rows=2, colors='p_gatling',
        #                                 initial_y=0, initial_x=self.screen_width - 50, x_speed=-1, y_speed=1)
        #     enemy2.enemy_y_speed_countdown = 1000
        #     enemy2.enemy_y_speed_drop_time = 3
        #     self.append_enemy(enemy1)
        #     self.append_enemy(enemy2)
        #
        # elif dif >= 10000 and self.spawned_waves == 4:
        #     enemies = \
        #         deploy.enemy_row_deploy(cols=5, colors='p_gatling',
        #                                 initial_y=0, initial_x=20, x_speed=2, y_speed=2, col_distance=100)
        #     enemies.enemy_y_speed_countdown = 0
        #     enemies.enemy_y_speed_drop_time = 0
        #     self.append_enemy(enemies)
        #
        # elif dif >= 12000 and self.spawned_waves == 5:
        #     enemies = \
        #         deploy.enemy_row_deploy(cols=5, colors='p_gatling',
        #                                 initial_y=0, initial_x=self.screen_width / 2, x_speed=0, y_speed=2,
        #                                 col_distance=100)
        #     enemies.enemy_y_speed_countdown = 0
        #     enemies.enemy_y_speed_drop_time = 0
        #     enemies2 = \
        #         deploy.enemy_row_deploy(cols=5, colors='p_gatling',
        #                                 initial_y=self.screen_height, initial_x=self.screen_width / 2, x_speed=0, y_speed=-1,
        #                                 col_distance=100)
        #     enemies2.enemy_y_speed_countdown = 0
        #     enemies2.enemy_y_speed_drop_time = 0
        #     self.append_enemy([enemies, enemies2])
