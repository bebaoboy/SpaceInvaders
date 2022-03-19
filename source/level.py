import math
import random
import sys

import pygame
import source.block as block
import source.enemy as enemy
import source.enemy_deploy as deploy
import source.laser as laser
import source.explosion as explosion
import source.collectibles as collectibles
from source.display_ingame_text import display_ingame_text


class Level:
    def __init__(self, display,
                 width, height, players, clock, sound_controller, font, tip, name, coins=0, score=0,
                 hp=0):
        self.current_timing = 0
        self.level_name = name
        self.level_code = ''
        self.clock = clock
        self.timer = 0
        self.font: pygame.font.Font = font
        self.tip = tip
        self.end_level_hint = ''
        self.finished_intro = False
        self.intro = ''
        self.intro_timer = 0
        self.intro_time = 1800

        self.laser_surf = pygame.Surface((4, 20)).convert_alpha()

        self.player = players
        self.screen_width = width
        self.screen_height = height

        self.crt = display['crt']
        self.screen = display['screen']
        self.pause_panel = display['pause_panel']
        self.pause_button = pygame.sprite.GroupSingle(display['pause_button'])

        self.sound_controller = sound_controller

        self.in_game_hint = [
            # min, max time, *args
            [0, 5000, 'red is fragile', 200, self.screen_height / 2]
        ]

        # player
        self.player_mlee_dmg = 50
        self.score_factor = 1.0
        # NO_EDIT
        self.score = score

        self.player_max_health = 4000
        self.player_health = \
            min(hp + self.player_max_health / 4, self.player_max_health) if hp != 0 else self.player_max_health

        self.health_bar_length = 300
        self.health_ratio = self.health_ratio = self.player_max_health / self.health_bar_length
        self.player_mlee_timer = 0
        self.player_mleed = False
        self.player_mlee_countdown = 5000

        # bullets
        self.laser_countdown = 875
        self.laser_speed = -8
        self.laser_speed_rate = 1.0375
        self.laser_dmg = 50
        self.laser_type = 1
        # NO_EDIT
        self.laser_speed_score = 50 + self.score
        self.laser_countdown_rate = -25
        self.laser_min_countdown = 50
        self.laser_max_speed = -30
        self.lasers = pygame.sprite.Group()

        self.equipment_speed = -8
        self.equipment_dmg = 90
        self.equipment_cooldown = 750
        self.equipment_type = 2
        # NO_EDIT
        self.equipment_is_ready = True
        self.equipment_timer = 0
        self.equipment_bullets = pygame.sprite.Group()

        # block
        self.block_size = 7
        # NO_EDIT
        self.block_shape = block.shape
        self.whole_block_size = self.block_size * 13
        self.block_amount = 0
        self.blocks = [pygame.sprite.Group()]
        self.min_space_between = 100
        self.max_space_between = 200

        # enemy
        # NO_EDIT
        self.enemy_y_speed_rate = 1
        self.died_enemies = 0

        self.enemy_laser = pygame.sprite.Group()

        # extra enemy
        self.extra_enemy_spawn_min_time = 7000
        self.extra_enemy_spawn_max_time = 15000
        self.extra_enemy_spawn_time = random.randint(self.extra_enemy_spawn_min_time, self.extra_enemy_spawn_max_time)
        self.extra_enemy_timer = 0
        self.extra_enemy_speed = 3
        # NO_EDIT
        self.extra_enemy = pygame.sprite.GroupSingle()
        self.extra_enemy_bonus = 50
        self.extra_enemy_health = 60

        # explosions
        self.explosions = pygame.sprite.Group()
        self.enemy_explosion_timer = 0

        # collectibles
        self.collectibles = pygame.sprite.Group()
        self.collectible_speed = 1
        self.coin_rate = 2
        self.coins = coins
        self.coin = collectibles.Coin(75, 46, self.screen_width, self.screen_height, 0)
        self.coin.time_to_live = -1
        self.collectibles.add(self.coin)

        # LEVEL
        self.mouse_clicked = False
        self.is_paused = False
        self.old_timing = self.current_timing
        self.end_level = False
        self.save_level = False
        self.game_over = False
        self.enemies = [enemy.EnemyArmy([[enemy.Enemy()]], [['']], 0)]
        self.enemies.clear()
        self.enemy_amount = 0
        self.spawned_waves = 0
        self.max_waves = 1
        self.spawn_timer = self.current_timing
        self.end_level_timer = self.current_timing
        self.finished_timer = False

        self.make_multiple_blocks(max_space_between=self.max_space_between, min_space_between=self.min_space_between)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if not self.end_level and not self.game_over and self.equipment_is_ready:
            if keys[pygame.K_SPACE]:
                self.equipment_shoot(self.equipment_type)
                self.equipment_is_ready = False
                self.sound_controller.play_sound('laser')
                self.equipment_timer = self.current_timing
            elif keys[pygame.K_q]:
                self.game_over = True
            elif keys[pygame.K_s]:
                self.save_level = True
                self.old_timing = self.current_timing

        if self.mouse_clicked:
            if pygame.mouse.get_pressed()[0] and self.pause_button.sprite.rect.collidepoint(pygame.mouse.get_pos()):
                self.is_paused = True
                print('CLICKED')
            elif pygame.mouse.get_pressed()[0] and self.is_paused:
                if not self.pause_panel.rect.collidepoint(pygame.mouse.get_pos()):
                    self.save_level = False
                    self.end_level = False
                    self.is_paused = False
                    self.current_timing = self.old_timing
                    self.finished_timer = False
                    print(f'score = {self.score}, time={self.old_timing}')
                    print('UNCLICKED')
        if self.is_paused:
            b = self.pause_panel.clicked(self.current_timing)  # QUIT OR SAVE
            if b == -1:
                self.is_paused = False
                self.save_level = False
                self.game_over = True
                self.old_timing = self.current_timing
            elif b == 1:
                self.save_level = True
                self.is_paused = False

            self.mouse_clicked = False

    def welcome_screen(self):
        if self.current_timing - self.intro_timer >= self.intro_time:
            self.finished_intro = True
        else:
            display_ingame_text(self.screen, self.font, f'{self.level_name}',
                                self.screen_width / 2, self.screen_height / 2 - 100, 1.5, 1.5)
            display_ingame_text(self.screen, self.font, self.intro,
                                self.screen_width / 2, self.screen_height / 2, 0.8, 0.8,
                                color='light blue')

    def check(self):
        if self.end_level or self.game_over:
            if not self.save_level:
                self.destroy()
            print(f'end {self.level_name}, score = {self.score}, time={self.old_timing}')

    def draw(self):
        try:
            self.screen.fill((30, 30, 30))

            # main drawing
            self.player.draw(self.screen)

            if not self.finished_intro:
                self.welcome_screen()
            else:
                if not self.end_level and not self.game_over:

                    for block_ in self.blocks:
                        block_.draw(self.screen)

                    for enemies in self.enemies:
                        for enemy_row in enemies.enemy_packs:
                            for enemy_col in enemy_row:
                                if enemy_col is not None:
                                    self.enemy_health_draw(enemy_col)
                                    if enemy_col.another_img is not None:
                                        self.screen.blit(enemy_col.another_img, enemy_col.another_rect)
                                    else:
                                        enemy_col.sp.draw(self.screen)

                    self.explosions.update(self.current_timing, self.screen)

                    self.lasers.draw(self.screen)
                    self.equipment_bullets.draw(self.screen)
                    self.enemy_laser.draw(self.screen)
                    self.extra_enemy.draw(self.screen)
                    self.collectibles.draw(self.screen)

                    if self.is_paused:
                        self.pause_panel.draw()
                        pygame.time.wait(1)

                else:
                    print('end screen')
                    display_ingame_text(self.screen, self.font, f'end {self.level_name}.',
                                        self.screen_width / 2, self.screen_height / 2 - 110, 1.55, 1.55)
                    display_ingame_text(self.screen, self.font, f'{self.end_level_hint}',
                                        self.screen_width / 2, self.screen_height / 2 - 40, 0.75, 0.75,
                                        color='light blue')
                    display_ingame_text(self.screen, self.font, f'tips: {self.tip}',
                                        self.screen_width / 2, self.screen_height / 2 + 110, 0.75, 0.75)
                    if self.end_level:
                        display_ingame_text(self.screen, self.font, f'Loading next level...',
                                            self.screen_width / 2, self.screen_height / 2 + 170,
                                            0.5, 0.5)
                    else:
                        display_ingame_text(self.screen, self.font, f'Game over',
                                            self.screen_width / 2, self.screen_height / 2 + 170,
                                            0.5, 0.5)
                    self.collectibles.draw(self.screen)

                    if self.current_timing - self.end_level_timer >= 3000:
                        self.finished_timer = True
                        return

            self.health_bar_draw()
            self.score_draw()
            self.pause_button.draw(self.screen)

        # pygame.display.flip()
        except pygame.error as err:
            print(err)
            sys.exit()

    def update(self):
        self.get_input()
        self.player.update(pygame.mouse.get_pos()[0])

        if not self.is_paused:
            if not self.end_level and not self.game_over and self.finished_intro:
                if self.current_timing - self.timer >= self.laser_countdown:
                    self.laser_shoot(self.laser_type)
                    self.timer = self.current_timing
                    # self.sound_controller.play_sound('laser')

                self.equipment_recharge()
                self.equipment_bullets.update(self.current_timing)
                self.lasers.update(self.current_timing)

                for laser_ in self.lasers:
                    if len(laser_.__getattribute__('laser_list')) != 0:
                        for child_laser in laser_.__getattribute__('laser_list'):
                            self.lasers.add(child_laser)

                self.extra_enemy_spawn()
                self.extra_enemy.update()

                self.special()

                self.enemy_checker()
                self.collision_check()

                if self.player_health > self.player_max_health:
                    self.player_health = self.player_max_health
                if self.player_health <= 0:
                    self.player_health = 0
                    self.game_over = True

                # if self.enemies and not self.end_level and not self.game_over:
                # 
                # print(f'enemy cooldown {current_timing - self.enemy_cooldown_timer}')

                # if current_timing - self.enemy_cooldown_timer >= self.enemy_cooldown:
                #     self.enemy_shoot()
                #     self.enemy_cooldown_timer = current_timing
                for idx, enemies in enumerate(self.enemies):
                    if self.current_timing - enemies.enemy_cooldown_timer >= enemies.enemy_shoot_cooldown:
                        enemies.enemy_cooldown_timer = self.current_timing
                        self.enemy_shoot(idx)

                for laser_ in self.enemy_laser:
                    if len(laser_.__getattribute__('laser_list')) != 0:
                        for child_laser in laser_.__getattribute__('laser_list'):
                            self.enemy_laser.add(child_laser)

                self.enemy_laser.update(self.current_timing)
                self.enemy_move_down_cooldown()
                self.enemy_move_x_cooldown()
                for enemies in self.enemies:
                    enemies.update(self.current_timing, 0, 0)
                self.mlee_check()
                self.end_level_timer = self.current_timing

            self.collectible_check()
            self.old_timing = self.current_timing

        self.current_timing += 15.5

    # LASER STUFF
    def laser_shoot(self, types=1, dmg=-1):
        if self.score >= self.laser_speed_score:
            if abs(self.laser_speed) <= abs(self.laser_max_speed):
                self.laser_speed *= self.laser_speed_rate

            if self.laser_countdown > self.laser_min_countdown:
                self.laser_countdown \
                    += self.laser_countdown_rate * (0.88 + abs(self.laser_speed / self.laser_max_speed))
                if self.laser_countdown < self.laser_min_countdown:
                    self.laser_countdown = self.laser_min_countdown

            print(f'laser speed = {self.laser_speed}, laser cd = {self.laser_countdown}')
            self.laser_speed_score *= 1.75

        if dmg < 0:
            dmg = self.laser_dmg

        for laser_ in laser.get_player_laser(types, self.player.sprite.rect, self.current_timing, self.laser_surf,
                                             dmg, self.laser_speed,
                                             self.screen_width, self.screen_height):
            self.lasers.add(laser_)

    def equipment_shoot(self, types):
        print('equipment shooting')
        for bullets in laser.get_player_laser(
                types, self.player.sprite.rect, self.current_timing,
                self.laser_surf, self.equipment_dmg, self.equipment_speed,
                self.screen_width, self.screen_height):
            self.equipment_bullets.add(bullets)
        # self.equipment_bullets.add(laser.Laser(pos, 0, self.screen_width, 0, self.player.sprite.rect.bottom,
        #                                        dmg, self.equipment_speed))

    def equipment_recharge(self):
        if not self.equipment_is_ready:
            if self.current_timing - self.equipment_timer >= self.equipment_cooldown:
                self.equipment_is_ready = True

    # BLOCKS
    def make_blocks(self, initial_x, initial_y, block_size=0, shape=None, color='green'):
        list_of_blocks = []
        if block_size == 0:
            block_size = self.block_size
        if shape is None:
            shape = self.block_shape
        for r_idx, row in enumerate(shape):
            for c_idx, col in enumerate(row):
                if col == 'x':
                    x = initial_x + c_idx * block_size
                    y = initial_y + r_idx * block_size
                    list_of_blocks.append(block.Block(color, block_size, x, y))

        self.blocks.append(pygame.sprite.Group(list_of_blocks))
        speed = random.choice([-1, -2, 1, 2])
        for blocks in self.blocks[len(self.blocks) - 1].sprites():
            blocks.__setattr__('x_speed', speed)

    def make_multiple_blocks(self, initials=None, max_space_between=200, min_space_between=100,
                             block_size=None, shape=None, color='green'):
        if block_size is None:
            block_size = self.block_size
        if shape is None:
            shape = block.shape

        min_y_offset = self.screen_height - 180
        max_y_offset = self.screen_height - 110

        if max_space_between > self.screen_width or min_space_between < 0:
            return

        if initials is None:
            initials = [(random.randint(-40, 45),
                         random.randint(min_y_offset, max_y_offset)),
                        (random.randint(self.screen_width - self.whole_block_size - 45,
                                        self.screen_width - self.whole_block_size + 40),
                         random.randint(min_y_offset, max_y_offset))]

        if len(initials) == 0:
            prev_x = -50
            distance = self.screen_width - prev_x + 30
        else:
            prev_x = initials[0][0] + self.whole_block_size
            distance = initials[1][0] - prev_x - 30  # distance btw the two

        self.block_amount = math.floor(distance / self.whole_block_size) + 1

        while max_space_between < min_space_between:
            self.block_amount -= 1
            spare_space = distance - self.block_amount * self.whole_block_size
            max_space_between = spare_space / self.block_amount

        max_space_between = math.floor(max_space_between)
        for _ in range(self.block_amount):
            x = random.randint(prev_x + min_space_between, prev_x + max_space_between)
            if x + self.whole_block_size >= distance - 30:
                self.block_amount = len(initials)
                break
            initials.append((x, random.randint(min_y_offset, max_y_offset)))
            prev_x = initials[len(initials) - 1][0] + self.whole_block_size

        for initial in initials:
            self.make_blocks(initial[0], initial[1], block_size, shape, color)

        self.block_amount += 2
        print(f'num of blocks: {self.block_amount}')

        # for block_ in self.blocks:
        #     for blocks in block_.sprites():
        #         if blocks.rect.centerx > self.screen_width / 2:
        #             blocks.__setattr__('x_speed', -1)
        #         else:
        #             blocks.__setattr__('x_speed', 2)

    def moving_blocks(self):
        x_left_constraint = 0
        x_right_constraint = self.screen_width
        # y_upper_constraint = self.screen_height - 300
        # y_lower_constraint = self.screen_height
        for block_ in self.blocks:
            for blocks in block_.sprites():
                if blocks.rect.centerx < x_left_constraint:
                    # blocks.centerx = x_left_constraint + 2
                    blocks.rect.centerx = blocks.rect.centerx - x_left_constraint + x_right_constraint
                elif blocks.rect.centerx > x_right_constraint:
                    # blocks.rect.centerx = x_right_constraint - 2
                    blocks.rect.centerx %= x_right_constraint

        for block_ in self.blocks:
            for blocks in block_.sprites():
                blocks.update()
            # if blocks.top < y_upper_constraint:
            #     blocks.centery = y_upper_constraint + 2
            #     blocks.y_speed = abs(blocks.y_speed)
            # elif blocks.bottom > y_lower_constraint:
            #     blocks.centery = y_lower_constraint - 2
            #     blocks.y_speed = -abs(blocks.y_speed)

    # ENEMY
    def append_enemy(self, enemy_packs):
        if type(enemy_packs) is enemy.EnemyArmy:
            if enemy_packs.enemy_x_left_constraint is None:
                enemy_packs.enemy_x_left_constraint = -15
            if enemy_packs.enemy_x_right_constraint is None:
                enemy_packs.enemy_x_right_constraint = self.screen_width + 15
            self.enemies.append(enemy_packs)
            self.enemy_amount += enemy_packs.enemy_amount
        else:
            for enemies in enemy_packs:
                if enemies.enemy_x_left_constraint is None:
                    enemies.enemy_x_left_constraint = -15
                if enemies.enemy_x_right_constraint is None:
                    enemies.enemy_x_right_constraint = self.screen_width + 15
                self.enemies.append(enemies)
                self.enemy_amount += enemies.enemy_amount
        self.spawned_waves += 1

    def enemy_move_down_cooldown(self):
        for enemies in self.enemies:
            # print(f'enemy move down: {self.current_timing - self.enemy_y_timer}, drop timer = {
            # self.enemy_y_speed_drop_time}')
            if (not enemies.enemy_move_down_already
                and self.current_timing - enemies.enemy_y_timer >= enemies.enemy_y_speed_countdown) \
                    or (enemies.enemy_y_speed_drop_time != 0 and enemies.enemy_move_down_already):
                enemies.enemy_y_speed_drop_time -= 1
                if math.floor(enemies.enemy_y_speed_drop_time) == 0:
                    enemies.enemy_y_speed_drop_time = enemies.enemy_y_speed_drop_rate
                    enemies.enemy_move_down_already = True
                    enemies.enemy_y_timer = self.current_timing

                # for enemy_row in enemies.enemy_packs:
                #     for enemy_col in enemy_row:
                #         if enemy_col is not None:
                #             enemy_col.update(0, enemies.enemy_y_speed)
                enemies.update(self.current_timing, 0, enemies.enemy_y_speed)

    def enemy_move_x_cooldown(self):
        for enemies in self.enemies:
            # print(f'enemy move down: {self.current_timing - self.enemy_y_timer}, drop timer = {
            # self.enemy_y_speed_drop_time}')
            if (not enemies.enemy_move_x_already
                and self.current_timing - enemies.enemy_x_timer >= enemies.enemy_x_speed_countdown) \
                    or (enemies.enemy_x_speed_drop_time != 0 and enemies.enemy_move_x_already):
                enemies.enemy_x_speed_drop_time -= 1
                if math.floor(enemies.enemy_x_speed_drop_time) == 0:
                    enemies.enemy_x_speed_drop_time = enemies.enemy_x_speed_drop_rate
                    enemies.enemy_move_x_already = True
                    enemies.enemy_x_timer = self.current_timing

                # for enemy_row in enemies.enemy_packs:
                #     for enemy_col in enemy_row:
                #         if enemy_col is not None:
                #             enemy_col.update(enemies.enemy_x_speed, 0)
                enemies.update(self.current_timing, enemies.enemy_x_speed, 0)

    def enemy_shoot(self, idx):
        if self.enemies[idx].enemy_amount == 0:
            return
        row = random.randint(0, len(self.enemies[idx].enemy_packs) - 1)
        col = random.randint(0, len(self.enemies[idx].enemy_packs[row]) - 1)
        while self.enemies[idx].enemy_packs[row][col] is None:
            row = random.randint(0, len(self.enemies[idx].enemy_packs) - 1)
            col = random.randint(0, len(self.enemies[idx].enemy_packs[row]) - 1)
        color = self.enemies[idx].enemy_packs[row][col].color
        print(f'color chosen: {color}')

        if color.split('_')[0] in deploy.enemy_stat:
            if self.current_timing - self.enemies[idx].enemy_packs[row][col].timer \
                    >= self.enemies[idx].enemy_packs[row][col].cooldown \
                    or self.enemies[idx].enemy_packs[row][col].timer == 0:
                self.enemies[idx].enemy_packs[row][col].timer = self.current_timing
                print('shoot')

                speed_y = self.enemies[idx].enemy_laser_speed * (0.2 + abs(self.laser_speed / self.laser_max_speed))

                # laser is different for each color
                for laser_ in laser.get_player_laser(color, self.enemies[idx].enemy_packs[row][col].sp.sprite.rect,
                                                     self.current_timing, self.laser_surf,
                                                     self.enemies[idx].enemy_packs[row][col].dmg, speed_y,
                                                     self.screen_width, self.screen_height):
                    self.enemy_laser.add(laser_)

    def extra_enemy_spawn(self):
        speed = self.extra_enemy_speed * (0.88 + abs(self.laser_speed / self.laser_max_speed))
        side = random.choice(['right', 'left'])
        if side == 'right':
            speed = -abs(speed)
        height = random.choice([random.randint(10, 25),
                                random.randint(self.screen_height - 380, self.screen_height - 220)])
        if self.current_timing - self.extra_enemy_timer >= self.extra_enemy_spawn_time:
            if len(self.extra_enemy) == 0:
                self.extra_enemy.add(enemy.ExtraEnemy(speed, side, self.screen_width, height, self.extra_enemy_health))
                print(f'extra: speed = {speed}, side = {side}')

            self.extra_enemy_spawn_time = random.randint(self.extra_enemy_spawn_min_time,
                                                         self.extra_enemy_spawn_max_time)
            self.extra_enemy_timer = self.current_timing

    # CHECKER
    def enemy_checker(self):
        if self.save_level or self.spawned_waves == self.max_waves and self.died_enemies == self.enemy_amount:
            self.end_level = True
            return

        for enemies in self.enemies:
            if len(enemies.enemy_packs) == 0:
                continue
            if enemies.enemy_move_down_already:
                enemies.enemy_move_down_already = False

            if enemies.enemy_move_x_already:
                enemies.enemy_move_x_already = False

            enemies_out_of_sight = True

            for row_idx, enemy_row in enumerate(enemies.enemy_packs):
                for col_idx, enemy_col in enumerate(enemy_row):
                    if enemy_col is not None:
                        if (enemy_col.sp.sprite.rect.centerx >= enemies.enemy_x_right_constraint) \
                                and enemies.enemy_x_speed > 0.0:
                            enemies.enemy_x_speed = -abs(enemies.enemy_x_speed)

                        elif (enemy_col.sp.sprite.rect.centerx <= enemies.enemy_x_left_constraint) \
                                and enemies.enemy_x_speed < 0.0:
                            enemies.enemy_x_speed = abs(enemies.enemy_x_speed)

                        if enemies.enemy_y_upper_constraint is not None and (
                                enemy_col.sp.sprite.rect.centery >= enemies.enemy_y_upper_constraint) \
                                and enemies.enemy_y_speed > 0.0:
                            enemies.enemy_y_speed = -abs(enemies.enemy_y_speed)

                        elif enemies.enemy_y_lower_constraint is not None and (
                                enemy_col.sp.sprite.rect.centery <= enemies.enemy_y_lower_constraint) \
                                and enemies.enemy_y_speed < 0.0:
                            enemies.enemy_y_speed = abs(enemies.enemy_y_speed)

                        if enemy_row[col_idx].hp <= 0:
                            self.score += enemy_row[col_idx].score * self.score_factor
                            enemies.kill(row_idx, col_idx)
                            enemies.enemy_amount -= 1
                            self.died_enemies += 1
                            self.explosions.add(
                                explosion.EnemyExplosion(self.current_timing,
                                                         enemy_col.color,
                                                         enemy_col.sp.sprite.rect.centerx,
                                                         enemy_col.sp.sprite.rect.centery,
                                                         enemy_col.sp.sprite.image.get_width(),
                                                         enemy_col.sp.sprite.image.get_height()))
                            rand_num = random.randint(0, self.coin_rate)
                            if rand_num == 0:
                                self.collectibles.add(
                                    collectibles.Coin(enemy_col.sp.sprite.rect.centerx,
                                                      enemy_col.sp.sprite.rect.centery,
                                                      self.screen_width, self.screen_height, self.collectible_speed)
                                )
                            print(f'killed = {self.died_enemies}')
                            self.sound_controller.play_sound('enemy_explosion')

                        if enemy_col.sp.sprite.rect.top <= self.screen_height \
                                and enemy_col.sp.sprite.rect.bottom >= 0 \
                                and enemy_col.sp.sprite.rect.topright[0] >= 0 \
                                and enemy_col.sp.sprite.rect.topleft[0] <= self.screen_width:
                            enemies_out_of_sight = False

            if enemies_out_of_sight:
                self.died_enemies += enemies.enemy_amount
                enemies.enemy_amount = 0
                print('out of sight')
                enemies.enemy_packs.clear()

    def collision_check(self):
        block_hit = False
        # player laser
        for laser_ in self.lasers:
            # block
            for blocks in self.blocks:
                if pygame.sprite.spritecollide(laser_, blocks, True):
                    laser_.kill()
                    block_hit = True

            if self.extra_enemy.sprite is not None and pygame.sprite.collide_rect(laser_, self.extra_enemy.sprite):
                laser_.kill()
                self.extra_enemy.sprite.__setattr__('hp',
                                                    self.extra_enemy.sprite.__getattribute__('hp') - self.laser_dmg)

        # equipment laser
        for equipment in self.equipment_bullets:
            for blocks in self.blocks:
                if pygame.sprite.spritecollide(equipment, blocks, True):
                    equipment.kill()
                    block_hit = True

            if self.extra_enemy.sprite is not None and pygame.sprite.collide_rect(equipment, self.extra_enemy.sprite):
                equipment.kill()
                self.extra_enemy.sprite.__setattr__('hp',
                                                    self.extra_enemy.sprite.__getattribute__('hp') - self.equipment_dmg)

        # extra enemy
        if self.extra_enemy.sprite is not None and self.extra_enemy.sprite.__getattribute__('hp') <= 0:
            # self.player_health += random.randint(self.extra_enemy_bonus + 100, self.extra_enemy_bonus + 200)
            self.collectibles.add(collectibles.HealthBag(
                self.extra_enemy.sprite.rect.x,
                self.extra_enemy.sprite.rect.y,
                self.screen_width, self.screen_height,
                random.randint(self.extra_enemy_bonus + 50, self.extra_enemy_bonus + 200),
                random.randint(3, 5))
            )
            self.extra_enemy.sprite.kill()
            self.sound_controller.play_sound('extra_hit')

            # for enemy_row in self.enemies:
            #     for col_idx, enemy_col in enumerate(enemy_row):
            #         if enemy_row[col_idx] is not None \
            #                 and pygame.sprite.collide_rect(equipment, enemy_col.sp.sprite):
            #             if enemy_row[col_idx].hp > 0:
            #                 enemy_row[col_idx].hp -= equipment.__getattribute__('dmg')
            #
            #             equipment.kill()

        # enemy laser
        for laser_ in self.enemy_laser:
            for blocks in self.blocks:
                if pygame.sprite.spritecollide(laser_, blocks, True):
                    laser_.kill()
            if pygame.sprite.collide_rect(laser_, self.player.sprite):
                laser_.kill()
                self.player_health -= laser_.__getattribute__('dmg')
                print(f'hp = {self.player_health}')
                self.explosions.add(explosion.EnemyExplosion(self.current_timing, 'w',
                                                             laser_.rect.midbottom[0],
                                                             laser_.rect.midbottom[1],
                                                             self.player.sprite.image.get_width() * 0.5,
                                                             self.player.sprite.image.get_height() * 0.6))

        if block_hit:
            self.sound_controller.play_sound('block')

        # enemy - player
        for enemies in self.enemies:
            for enemy_row in enemies.enemy_packs:
                for col_idx, enemy_col in enumerate(enemy_row):
                    if enemy_row[col_idx] is not None \
                            and pygame.sprite.collide_rect(self.player.sprite, enemy_col.sp.sprite) \
                            and not enemy_row[col_idx].mleed and not self.player_mleed:
                        self.player_mleed = True
                        enemy_row[col_idx].mleed = True
                        self.player_health -= enemy_row[col_idx].mlee_dmg
                        self.player_mlee_timer = 0
                        print(f'player mlee = {enemy_row[col_idx].color}, hp={enemy_row[col_idx].hp}')
                        enemy_row[col_idx].hp -= self.player_mlee_dmg
                        enemy_row[col_idx].mlee_timer = 0

                    for laser_ in self.lasers:
                        if enemy_row[col_idx] is not None \
                                and pygame.sprite.collide_rect(laser_, enemy_col.sp.sprite):
                            if enemy_row[col_idx].hp > 0:
                                enemy_row[col_idx].hp -= laser_.__getattribute__('dmg')

                            laser_.kill()
                            self.sound_controller.play_sound('hit')
                    for equipment in self.equipment_bullets:
                        if enemy_row[col_idx] is not None \
                                and pygame.sprite.collide_rect(equipment, enemy_col.sp.sprite):
                            if enemy_row[col_idx].hp > 0:
                                enemy_row[col_idx].hp -= equipment.__getattribute__('dmg')

                            equipment.kill()
                            self.sound_controller.play_sound('hit')

    def collectible_check(self):
        # player - collectibles
        for coll in pygame.sprite.spritecollide(self.player.sprite, self.collectibles, True):
            if type(coll) is collectibles.Coin:
                self.coins += 1
            elif type(coll) is collectibles.HealthBag:
                self.player_health += coll.__getattribute__('hp')
            self.sound_controller.play_sound('coin_hit')

        self.collectibles.update()

    def mlee_check(self):
        if self.player_mleed:
            if self.current_timing - self.player_mlee_timer >= self.player_mlee_countdown:
                self.player_mlee_timer = self.current_timing
                self.player_mleed = False
        for enemies in self.enemies:
            for enemy_row in enemies.enemy_packs:
                for col_idx, enemy_col in enumerate(enemy_row):
                    if enemy_col is not None and enemy_row[col_idx].mleed:
                        if self.current_timing - enemy_row[col_idx].mlee_timer >= enemy_row[col_idx].mlee_time:
                            enemy_row[col_idx].mlee_timer = self.current_timing
                            enemy_row[col_idx].mleed = False

    # DRAWING
    def health_bar_draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_width - self.health_bar_length, 23,
                                                    self.player_health / self.health_ratio, 10))

        score_surf = self.font.render(f'hp: {int(self.player_health)}'.upper(), False, 'white').convert_alpha()
        score_rect = score_surf.get_rect(topleft=(750, -5))
        self.screen.blit(score_surf, score_rect)

    def enemy_health_draw(self, enemy_col):
        if enemy_col.color.find('boss') != -1:
            bar_color = (240, 0, 0)
        else:
            bar_color = (128, 128, 128)
        if self.extra_enemy.sprite is not None:
            pygame.draw.rect(
                self.screen, (200, 0, 0),
                (self.extra_enemy.sprite.rect.topleft[0], self.extra_enemy.sprite.rect.topleft[1] - 5,
                 self.extra_enemy.sprite.__getattribute__('hp') /
                 (self.extra_enemy_health /
                  self.extra_enemy.sprite.image.get_width()), self.extra_enemy.sprite.image.get_height() * 0.1))

        if enemy_col.sp.sprite.rect.top < 30:
            pygame.draw.rect(
                self.screen, bar_color,
                (enemy_col.sp.sprite.rect.bottomleft[0], enemy_col.sp.sprite.rect.bottomleft[1] + 5,
                 enemy_col.hp / enemy_col.max_hp * enemy_col.sp.sprite.image.get_width(),
                 enemy_col.sp.sprite.image.get_height() * 0.1))
        else:
            pygame.draw.rect(
                self.screen, bar_color,
                (enemy_col.sp.sprite.rect.topleft[0], enemy_col.sp.sprite.rect.topleft[1] - 5,
                 enemy_col.hp / enemy_col.max_hp * enemy_col.sp.sprite.image.get_width(),
                 enemy_col.sp.sprite.image.get_height() * 0.1))

    def score_draw(self):
        score_surf = self.font.render(f'score: {int(self.score)}'.upper(), False, 'white').convert_alpha()
        score_rect = score_surf.get_rect(topleft=(10, -5))
        self.screen.blit(score_surf, score_rect)

        coin_surf = self.font.render(f'coin   : {int(self.coins)}'.upper(), False, 'white').convert_alpha()
        coin_rect = coin_surf.get_rect(topleft=(10, 30))
        self.screen.blit(coin_surf, coin_rect)

    # SPECIAL STUFF
    def destroy(self):
        self.extra_enemy.remove()
        self.enemies.clear()
        self.blocks.clear()
        self.lasers.remove()
        self.enemy_laser.remove()

    def special(self):
        pass

    def check_previous_wave(self):
        return self.enemies[len(self.enemies) - 1].enemy_amount == 0

    def reprJSON(self):
        self.clock = None
        self.font = None
        self.laser_surf = None

        self.player = None

        self.crt = None
        self.screen = None
        self.pause_panel = None
        self.pause_button = None

        self.sound_controller = None
        self.coin = None

        self.blocks = None
        self.extra_enemy = None

        dick = self.__dict__
        for name, val in dick.items():
            if type(val) is pygame.sprite.Group or type(val) is pygame.surface.Surface:
                dick[name] = None

        return {key: val for key, val in dick.items() if val is not None}
