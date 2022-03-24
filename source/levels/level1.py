import pygame

import source.level as level
import source.enemy_deploy as deploy
from source.display_ingame_text import display_ingame_text


class Level1(level.Level):
    def __init__(self, *pack):
        super().__init__(*pack)

        self.intro = 'a new beginning'
        
        colors = 'r'
        enemies = deploy.enemy_row_deploy(cols=8, colors=colors, initial_y=400, initial_x=0)
        enemies.enemy_y_speed_countdown = 1000
        self.append_enemy(enemies)
        self.laser_speed = -15
        self.laser_countdown = 600
        self.laser_type = 1
        self.blocks.clear()

        self.max_waves = 4

        self.end_level_hint = 'did you get the idea yet?'
        self.in_game_hint = [
            # text, min, max time
            [0, 5000, 'red is fragile', 200, self.screen_height / 2],
            [0, 5000, 'green is tough', 200, self.screen_height / 2],
            [0, 5000, 'blue is dangerous', 200, self.screen_height / 2],
            [0, 5000, 'yellow is for decoration', 400, self.screen_height / 2],
        ]

    def special(self):
        dif = self.current_timing - self.spawn_timer

        self.in_game_text()

        # timer
        # if dif < 8000 and self.enemies[len(self.enemies)-1].enemy_amount == 0:
        #     self.end_level = True

        if (dif >= 8000 or self.check_previous_wave()) and self.spawned_waves == 1:
            enemies = deploy.enemy_grid_deploy(rows=2, cols=7, colors='g', initial_y=220)
            enemies.enemy_y_speed_countdown = 1000
            self.laser_countdown = 300
            self.laser_type = 2
            self.spawn_timer = self.current_timing
            self.append_enemy(enemies)

        elif (dif >= 15000 or self.check_previous_wave()) and self.spawned_waves == 2:
            enemies = deploy.enemy_grid_deploy(cols=9, rows=3, colors='b', initial_y=180, initial_x=120)
            enemies.enemy_y_speed_countdown = 1000
            enemies.enemy_shoot_cooldown = 200
            enemies.enemy_y_speed_drop_time = 6
            enemies.enemy_y_speed_drop_rate = 5
            self.laser_type = 3
            self.laser_countdown = 200
            self.spawn_timer = self.current_timing
            self.append_enemy(enemies)

        elif (dif >= 8000 or self.check_previous_wave()) and self.spawned_waves == 3:
            enemies = deploy.enemy_row_deploy(cols=10, colors='y', initial_y=50, initial_x=100)
            enemies.enemy_y_speed_countdown = 50
            enemies.enemy_y_speed_drop_time = 3
            enemies.enemy_laser_speed *= 1.12
            enemies.enemy_y_speed_drop_time = 5
            enemies.enemy_y_speed_drop_rate = 5
            self.laser_type = 4
            self.laser_countdown = 300
            self.spawn_timer = self.current_timing
            self.append_enemy(enemies)

        # if self.spawned_waves == 1 and 0 <= dif <= 5000:
        #     display_ingame_text(self.screen, self.font,
        #                                            'red is fragile', 200, self.screen_height / 2)

    def in_game_text(self):
        dif = self.current_timing - self.spawn_timer
        idx = self.spawned_waves - 1

        if self.check_previous_wave():
            idx += 1

        if idx >= len(self.in_game_hint):
            return

        if len(self.in_game_hint[idx]) != 0:
            if self.check_previous_wave() or self.in_game_hint[idx][0] <= dif <= self.in_game_hint[idx][1]:
                display_ingame_text(self.screen, self.font, *self.in_game_hint[idx][2:])
