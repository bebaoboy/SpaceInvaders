import pygame.time
import source.level as level
import source.enemy_deploy as deploy


class Level9(level.Level):
    def __init__(self, *pack):
        super().__init__(*pack)
        self.intro = 'CLASSIC INVASION #4'
        colors = [
            ['b'] * 10,
            ['r'] * 10,
            [''] + ['y'] * 8 + [''],
            [''] + ['y'] * 8 + [''],
            [''] + ['r'] * 8 + [''],
            ['b'] * 10,
            ['g'] * 10
        ]
        enemies = \
            deploy.enemy_grid_deploy(rows=7, cols=10, colors=colors, initial_y=100)
        self.append_enemy(enemies)

        self.player_health += 1000

        self.laser_type = 6
        self.laser_speed = -16
        self.laser_countdown = 500
        self.laser_dmg = 75
        self.equipment_type = 3

        self.max_waves = 7

        self.max_space_between = 600
        self.max_space_between = 400
        self.blocks.clear()
        self.make_multiple_blocks(max_space_between=self.max_space_between, min_space_between=self.min_space_between)

    def special(self):
        dif = self.current_timing - self.spawn_timer
        # print(self.current_timing - self.spawn_timer)

        if dif >= 5000 and self.spawned_waves == 1:
            self.spawn_timer = self.current_timing
            colors = [
                [''] + ['r'] * 5 + [''],
                [''] + ['r'] * 5 + [''],
                [''] + ['r'] * 5 + ['']
            ]
            enemies = \
                deploy.enemy_grid_deploy(rows=3, cols=7, colors=colors, initial_y=50, x_speed=2, y_speed=1)
            enemies.enemy_y_speed_countdown = 0
            enemies.enemy_y_speed_drop_time = 0
            self.append_enemy(enemies)

        elif dif >= 7000 and self.spawned_waves == 2:
            enemy1 = \
                deploy.enemy_col_deploy(rows=5, colors='g', initial_y=0, initial_x=20, x_speed=0, y_speed=1)
            enemy1.enemy_y_speed_countdown = 1000
            enemy1.enemy_y_speed_drop_time = 3
            enemy2 = \
                deploy.enemy_col_deploy(rows=5, colors='g',
                                        initial_y=0, initial_x=self.screen_width - 50, x_speed=0, y_speed=1)
            enemy2.enemy_y_speed_countdown = 1000
            enemy2.enemy_y_speed_drop_time = 3
            self.append_enemy(enemy1)
            self.append_enemy(enemy2)

        elif dif >= 15000 and self.spawned_waves == 4:
            enemies = \
                deploy.enemy_row_deploy(cols=5, colors='y',
                                        initial_y=0, initial_x=20, x_speed=2, y_speed=2, col_distance=100)
            enemies.enemy_y_speed_countdown = 0
            enemies.enemy_y_speed_drop_time = 0
            self.append_enemy(enemies)

        elif dif >= 20000 and self.spawned_waves == 5:
            enemies = \
                deploy.enemy_row_deploy(cols=5, colors='y',
                                        initial_y=0, initial_x=self.screen_width - 50, x_speed=-2, y_speed=2,
                                        col_distance=100)
            enemies.enemy_y_speed_countdown = 0
            enemies.enemy_y_speed_drop_time = 0
            self.append_enemy(enemies)

        elif dif >= 25000 and self.spawned_waves == 6:
            self.laser_speed = -10
            self.laser_dmg = 100
            enemies = \
                deploy.enemy_row_deploy(cols=12, colors='r',
                                        initial_y=0, initial_x=0, x_speed=0.5, y_speed=0)
            enemies.enemy_laser_speed = 18
            enemies.enemy_shoot_cooldown = 18
            for enemy_row in enemies.enemy_packs:
                for enemy_col in enemy_row:
                    enemy_col.hp = enemy_col.max_hp = 1500
                    enemy_col.dmg = 10
            self.append_enemy(enemies)
