import random

import pygame.time

from source import block
from source.level import Level
from source.display_ingame_text import display_ingame_text
from source.enemy_deploy import enemy_col_deploy, enemy_grid_deploy, enemy_row_deploy, enemy_stat
from source.block import raining_shape, shape


class S_Level(Level):
    def __init__(self, *pack):
        super(S_Level, self).__init__(*pack)

        # special variable goes here
        # self.logo = ...

        self.level_code = ''

    def recover(self):
        pass


class BossLevel(S_Level):
    def __init__(self, *pack):
        super(S_Level, self).__init__(*pack)

        # special variable goes here
        # self.logo = ...
        self.intro = 'SHOW EM WHO"S BOSS'
        self.level_code = 'boss'


class MakeItRainLevel(S_Level):
    def __init__(self, *pack):
        super(S_Level, self).__init__(*pack)

        # special variable goes here
        # self.logo = ...

        self.level_code = 'make_it_rain'
        self.intro = 'MAKE IT RAIN'

        self.make_it_rain_idx = [0]

        self.raining_times = 5
        self.raining_times_counter = 1
        self.is_rained = False

        self.raining_time = 5000
        self.waiting_time = 7000
        self.start_raining_timer = 0

        self.raining_countdown = 150
        self.raining_timer = self.current_timing

        self.raining_shield = block.raining_shape

    def special(self):
        rain_dif = self.current_timing - self.start_raining_timer
        print(f'rain dif = {self.current_timing} - {self.start_raining_timer} = {rain_dif}')
        print(f'start = {self.start_raining_timer}')

        for idx in self.make_it_rain_idx:
            if self.enemies[idx].enemy_amount != 0 and self.raining_times_counter <= self.raining_times:
                if not self.is_rained:
                    if rain_dif >= self.waiting_time:
                        self.is_raining(idx)
                else:

                    self.crt.set_alpha(random.randint(1, 250))
                    self.screen.blit(self.crt, (-10, -10))
                    display_ingame_text(self.screen, self.font, 'MAKE IT RAIN!',
                                        450, self.screen_height / 2 - 50, 2, 2)

                    if rain_dif >= self.raining_time:
                        self.is_not_raining()
            else:
                self.make_it_rain_idx.pop(idx)

        self.moving_blocks()
        if len(self.make_it_rain_idx) == 0:
            self.done_raining()
            display_ingame_text(self.screen, self.font, 'MAKE IT RAIN!',
                                450, self.screen_height / 2 - 50, 2, 2)

    def is_raining(self, idx):
        pass

    def is_not_raining(self):
        pass

    def done_raining(self):
        pass


class EndlessLevel(S_Level):
    def __init__(self, *pack):
        super().__init__(*pack)
        self.level_name = 'endless zone'
        self.level_code = 'endless'

        self.player_max_health = 10000
        if self.score == 0:
            self.player_health = self.player_max_health

        self.bosses = -1
        self.blocks_timer = self.current_timing
        self.blocks_time = random.randint(6000, 10000)
        self.max_waves = 1
        self.max_enemy_group = 10

        self.backup_score = 0

        self.spawn_shapes = [
            [
                ['x'] * 7,
                [''] + ['x'] * 5 + [''],
                [''] * 2 + ['x'] * 3 + [''] * 2,
                [''] * 3 + ['x'] + [''] * 3
            ],
            [
                ['x'] * 5,
                ['x'] + [''] * 3 + ['x'],
                ['x'] + [''] * 3 + ['x'],
                ['x'] + [''] * 3 + ['x'],
                ['x'] * 5
            ],
            [
                ['x'] * 3,
                ['x'] + [''] + ['x'],
                ['x'] * 3
            ],
            [
                ['x'] + [''] + [''] + [''] + ['x'],
                [''] + ['x'] + [''] + ['x'] + [''],
                [''] + [''] + ['x'] + [''] + [''],
                [''] + ['x'] + [''] + ['x'] + [''],
                ['x'] + [''] + [''] + [''] + ['x']
            ],
            [
                ['x'] + [''] + ['x'],
                [''] + ['x'] + [''],
                ['x'] + [''] + ['x']
            ],
            [
                ['x'] + [''] + ['x'] + [''] + ['x'],
                [''] + ['x'] + [''] + ['x'] + ['']
            ],
            [
                [''] + [''] + ['x'] + [''] + [''],
                [''] + [''] + ['x'] + [''] + [''],
                ['x'] * 5,
                [''] + [''] + ['x'] + [''] + [''],
                [''] + [''] + ['x'] + [''] + ['']
            ],
            'row',
            'col',
            'grid'
        ]
        self.spawn_time = []
        self.boss_timer = self.current_timing
        self.boss_time = 25000
        self.spawn_time_list = [1000, 2000, 3200, 2500, 1650, 500, 2700, 4000, 5000]

    def spawn(self):
        self.max_waves += 1
        choice = random.randint(1, 2)
        choice2 = random.randint(1, 2)
        shapes = random.choice(self.spawn_shapes)
        if choice == 1:
            x_pos = random.randint(-50, 50)
            x_speed = random.choice([1, 2, 3])
        else:
            x_pos = random.randint(-50, self.screen_width - 10)
            x_speed = random.choice([-1, -2, -3])

        if choice2 == 1:
            y_pos = random.randint(-50, 200)
            y_speed = random.choice([0, 1, 2])
        else:
            y_pos = random.randint(self.screen_height - 300, self.screen_height - 150)
            y_speed = random.choice([0, -1, -2, -3])

        colors: str = random.choice(list(enemy_stat.keys()))
        row = random.randint(1, 7)
        col = random.randint(1, 9)

        enemies = None

        if colors.find('boss') == -1:
            if shapes == 'col':
                enemies = enemy_col_deploy(
                    rows=row, colors=colors,
                    initial_y=y_pos, initial_x=x_pos, x_speed=x_speed, y_speed=y_speed)
            elif shapes == 'row':
                enemies = enemy_row_deploy(
                    cols=col, colors=colors,
                    initial_y=y_pos, initial_x=x_pos, x_speed=x_speed, y_speed=y_speed)
            elif shapes == 'grid':
                row = random.randint(2, 4)
                col = random.randint(2, 8)

                enemies = enemy_grid_deploy(
                    rows=row, cols=col, colors=colors,
                    initial_y=y_pos, initial_x=x_pos, x_speed=x_speed, y_speed=y_speed)

            else:
                colors2: list = [_ for _ in list(enemy_stat.keys()) if _.find('boss') == -1]
                row = len(shapes)
                col = len(shapes[0])
                shapes2 = [[''] * col for _ in range(row)]
                choice = random.randint(1, 4)

                if choice == 1:
                    c = random.choice(colors2)
                    for i in range(len(shapes2)):
                        for j in range(len(shapes2[0])):
                            shapes2[i][j] = shapes[i][j]
                            if shapes2[i][j] == 'x':
                                shapes2[i][j] = c

                elif choice == 2 or choice == 3:
                    for i in range(len(shapes2)):
                        c = random.choice(colors2)
                        for j in range(len(shapes2[0])):
                            shapes2[i][j] = shapes[i][j]
                            if shapes2[i][j] == 'x':
                                shapes2[i][j] = c
                else:
                    for i in range(len(shapes2)):
                        for j in range(len(shapes[0])):
                            shapes2[i][j] = shapes[i][j]
                            if shapes2[i][j] == 'x':
                                c = random.choice(colors2)
                                shapes2[i][j] = c
                enemies = \
                    enemy_grid_deploy(rows=row, cols=col, colors=shapes2,
                                      initial_y=y_pos, initial_x=x_pos,
                                      x_speed=x_speed, y_speed=y_speed, col_distance=60)
        else:
            if self.current_timing - self.boss_timer >= self.boss_time:
                if self.bosses == -1:
                    self.boss_timer = self.current_timing
                    if self.spawned_waves % 20 == 0:
                        self.boss_time = min(10000, self.boss_time - 1000)
                    enemies = enemy_col_deploy(
                        rows=1, colors=colors,
                        initial_y=y_pos, initial_x=x_pos, x_speed=x_speed, y_speed=y_speed)
                    enemies_sprite = enemies.enemy_packs[0][0].sp.sprite
                    enemies.enemy_shoot_cooldown = 10
                    enemies_sprite.image = pygame.transform.scale(
                        enemies_sprite.image, (enemies_sprite.image.get_rect().width * 8,
                                               enemies_sprite.image.get_rect().height * 8))
                    enemies.enemy_packs[0][0].sp.sprite.rect = \
                        enemies.enemy_packs[0][0].sp.sprite.image.get_rect(topleft=(x_pos, y_pos))

                    enemies.enemy_packs[0][0].max_hp *= random.choice([0.2, 0.4])
                    enemies.enemy_packs[0][0].hp = enemies.enemy_packs[0][0].max_hp
                    enemies.enemy_packs[0][0].mlee_dmg = 10
                    if colors.find('rotate') != -1:
                        enemies.enemy_packs[0][0].rotate_speed = 30
                        enemies.enemy_packs[0][0].rotate_countdown = 6
                        enemies.enemy_packs[0][0].ani = None
                    self.bosses = len(self.enemies) - 1
                elif self.enemies[self.bosses].enemy_amount == 0:
                    self.bosses = -1
        if enemies:
            enemies.enemy_shoot_cooldown = random.randint(200, 1000)
            enemies.enemy_y_speed_countdown = random.randint(2000, 3000)
            enemies.enemy_laser_speed = random.randint(8, 15)

        # may do some rotations
        return enemies

    def player_change(self):
        self.laser_speed = random.randint(self.laser_max_speed, -9)
        self.laser_countdown = random.randint(self.laser_min_countdown + 80, 680)
        self.laser_dmg = random.randint(100, 250)
        self.laser_type = random.randint(2, 6)

        self.equipment_speed = random.randint(self.laser_max_speed, -8)
        self.equipment_dmg = random.randint(150, 350)
        self.equipment_cooldown = random.randint(350, 1200)
        self.equipment_type = random.randint(2, 6)

        self.extra_enemy_spawn_min_time = random.randint(3000, 7000)
        self.extra_enemy_bonus = random.randint(750, 1600)
        self.extra_enemy_health = random.randint(30, 150)
        self.collectible_speed = random.randint(1, 3)
        self.coin_rate = random.randint(0, 3)

    def block_change(self):
        self.blocks_time = random.randint(6000, 10000)
        self.blocks_timer = self.current_timing
        if self.player_health < self.player_max_health / 2:
            self.player_health += random.randint(1500, self.player_max_health // 3)
        block_size = random.randint(self.block_size - 1, self.block_size + 2)
        shape_ = random.choice([raining_shape, shape])
        self.blocks.clear()
        self.make_multiple_blocks(max_space_between=self.max_space_between,
                                  min_space_between=self.min_space_between,
                                  color=random.choice(['green', 'light blue', 'white', 'black',
                                                       'light blue', 'white', 'black', 'light green']),
                                  shape=shape_,
                                  block_size=block_size)

    def recover(self):
        self.score = self.backup_score

        if self.bosses != - 1:
            if self.enemies[self.bosses].enemy_amount != 0:
                self.enemies[self.bosses].enemy_packs[0][0].sp.sprite.image = pygame.transform.scale(
                    self.enemies[self.bosses].enemy_packs[0][0].sp.sprite.image, (
                        self.enemies[self.bosses].enemy_packs[0][0].sp.sprite.image.get_rect().width * 8,
                        self.enemies[self.bosses].enemy_packs[0][0].sp.sprite.image.get_rect().height * 8))
                self.enemies[self.bosses].enemy_packs[0][0].sp.sprite.rect = \
                    self.enemies[self.bosses].enemy_packs[0][0].sp.sprite.image.get_rect(topleft=(200, 100))

    def special(self):
        self.backup_score = self.score
        dif = self.current_timing - self.spawn_timer
        # print(self.current_timing - self.spawn_timer)

        if self.current_timing - self.blocks_timer >= self.blocks_time:
            self.player_change()
            self.block_change()

        if dif >= self.spawn_time or self.spawned_waves == 0 or self.enemies[len(self.enemies) - 1].enemy_amount == 0:
            self.spawn_timer = self.current_timing
            enemy_alive = 0
            for i in self.enemies:
                if len(i.enemy_packs) != 0:
                    enemy_alive += 1
            if enemy_alive <= self.max_enemy_group:
                enemies = self.spawn()
                if enemies:
                    self.append_enemy(enemies)
            self.spawn_time = random.choice(self.spawn_time_list)

        display_ingame_text(self.screen, self.font,
                            f'time: {int(self.current_timing / 1000)}',
                            self.screen_width / 2, 50, 0.8, 0.8)
        display_ingame_text(self.screen, self.font,
                            f'wave: {self.spawned_waves}',
                            self.screen_width / 2, 100, 0.8, 0.8)

        self.moving_blocks()
