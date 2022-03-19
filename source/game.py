import json
import sys
import random

import pygame
import cryptography.fernet as fernet

import source.menu as menu
import source.sound_controller as sound_controller
import source.resource_manager as resource_manager
import source.panel as panel
from source import level_grid, rng, gif_background, level
from source.player import Player
from source.resource_path import resource_path
from source.display_ingame_text import display_ingame_text
from source.enemy import Enemy, EnemyArmy


class SpaceInvaders:
    def __init__(self):
        pygame.init()

        self.screen_width = 900
        self.screen_height = 700
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.player = pygame.sprite.GroupSingle(
            Player((self.screen_width / 2, self.screen_height - 5), self.screen_width))
        self.clock = pygame.time.Clock()

        self.font_size = 20
        self.font_path = resource_path('font/Pixeled.ttf')
        self.font = pygame.font.Font(self.font_path, self.font_size)

        # resource
        self.crt = pygame.image.load(resource_path('graphics/tv.png')).convert_alpha()
        self.crt = pygame.transform.scale(self.crt, (self.screen_width + 10, self.screen_height + 10))
        self.crt_timer = pygame.time.get_ticks()
        self.is_crt = True
        self.loading_timer = None
        self.loading_panel = panel.LoadingPanel(self.font)
        self.is_loading = False

        pause_panel = panel.PausePanel(self.screen, self.font)

        self.display = {
            'screen': self.screen,
            'pause_panel': pause_panel,
            'pause_button': panel.PauseButton((10, 80)),
            'crt': self.crt
        }

        # sound
        self.sound_controller = sound_controller.SoundController()
        self.sound_controller.play_music()

        self.hp = 0
        self.score = 0
        self.coins = 0

        self.min_level = 1  # NO CHANGE PLS
        self.max_level = 10
        self.current_level = 11
        self.chosen_level = None

        self.loaded_level = None

        self.is_ready = True
        self.game_done = False
        self.is_choosing_level = False
        self.is_viewing_high_score = False
        self.counter = 0
        self.tips = [
            'press space to fire equipment',
            'press q to quit'
        ]

        # data
        self.resource_manager = resource_manager.ResourceManager()
        s = 'self.levels = [\n'
        for i in range(self.min_level, self.max_level + 1):
            s += f'\tlevel{i}.Level{i},\n'
        s += ']'

        self.resource_manager.exec_code(s)

        self.file_name = 'data.bin'
        self.key = fernet.Fernet(b'4WUlJJnPfhEk5zUQEhz4EasW8OajVbqAdGKhPeUrag4=')

        try:
            with open(resource_path(self.file_name), 'rb') as file:
                s = file.readline()
                s = self.key.decrypt(s).decode()
                l_split = s.split(',')
                self.coins, self.current_level = int(l_split[0]), int(l_split[1])
        except (Exception,):
            pass
        self.levels: list[type(level.Level)] = self.resource_manager.levels

        self.presaved_level = [{}] * self.max_level
        try:
            with open(resource_path('level.txt'), 'rb') as file:
                full = json.loads(self.key.decrypt(file.read()).decode())
                for obj in full:
                    if obj is not None:
                        level_num = int(obj['level_name'].split(' ')[1])
                        print(level_num)
                        self.presaved_level[level_num - 1] = obj
        except Exception as err:
            print(err)

        self.saved_level = [None] * self.max_level
        self.check_saved_level()

        # ui
        self.menu = menu.Menu('Courier New', self.font_size + 10,
                              self.screen, 100, 300)

        self.level_panel = level_grid.LevelGrid('Courier New', self.font_size + 10,
                                                self.screen, self.screen_width, self.screen_height,
                                                self.min_level, self.max_level, self.current_level)
        self.gif_background = gif_background.GifBackground(self.screen, self.screen_width, self.screen_height)

    def run(self):
        while True:
            try:
                self.gif_background.update()
                self.display_util()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.save_to_file()
                        pygame.quit()
                        sys.exit(0)

                    if self.is_ready:
                        if self.menu.menu_dict['quit'].clicked():
                            pygame.quit()
                            self.save_to_file()
                        if self.menu.menu_dict['mute_sound'].clicked():
                            if self.menu.menu_dict['mute_sound'].is_clicked:
                                self.sound_controller.mute_sound()
                            else:
                                self.sound_controller.unmute_sound()

                        if self.menu.menu_dict['mute_music'].clicked():
                            if self.menu.menu_dict['mute_music'].is_clicked:
                                self.sound_controller.mute_music()
                            else:
                                self.sound_controller.unmute_music()

                        if self.menu.menu_dict['crt'].clicked():
                            if self.menu.menu_dict['crt'].is_clicked:
                                self.is_crt = False
                            else:
                                self.is_crt = True

                        if self.menu.menu_dict['play'].clicked():
                            self.menu.menu_dict['play'].is_clicked = False
                            self.is_choosing_level = True
                            self.loading_timer = pygame.time.get_ticks()
                            self.is_loading = True
                            self.is_ready = False

                    if self.is_choosing_level:
                        current_timing = pygame.time.get_ticks()
                        # print(self.current_timing - self.loading_timer)
                        if self.is_loading and current_timing - self.loading_timer >= 500:
                            self.is_loading = False
                        if not self.is_loading:
                            self.chosen_level = self.level_panel.clicked()
                            if self.chosen_level is not None:
                                self.is_choosing_level = False

                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_q]:
                            self.reset()

                    if self.is_viewing_high_score:
                        pass

                    if self.game_done and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            print('======================DONE=====================')
                            self.save_info()
                            self.reset()

                # main game
                if not self.is_ready and not self.is_choosing_level and not self.game_done:
                    self.counter = self.chosen_level

                    pack = [self.display, self.screen_width, self.screen_height, self.player,
                            self.clock, self.sound_controller, self.font, random.choice(self.tips)]

                    for i in range(self.chosen_level, self.max_level + 1):
                        self.sound_controller.play_music(i)

                        # loaded_level = \
                        #     self.resource_manager.import_level_by_name(f'source.levels.level{i}', f'Level{i}')
                        if self.saved_level[i - 1] is not None:
                            self.loaded_level = self.saved_level[i - 1]
                            self.loaded_level.is_paused = True
                            self.loaded_level.score = max(self.loaded_level.score, self.score)
                            self.loaded_level.player_health = max(self.loaded_level.player_health, self.hp)
                            self.loaded_level.end_level = False
                            self.saved_level[i - 1] = None
                        else:
                            self.loaded_level = self.levels[i - 1]
                            self.loaded_level = self.loaded_level(*pack, f'level {i}', self.coins, self.score, self.hp)

                        self.level_run()

                        if self.loaded_level.end_level and not self.loaded_level.save_level\
                                and self.counter < self.max_level:
                            self.counter += 1
                            self.save_info()
                        else:
                            if self.counter == self.max_level and not self.loaded_level.game_over:
                                self.current_level = self.max_level + 1
                            if self.loaded_level.save_level:
                                self.saved_level[i - 1] = self.loaded_level
                            self.game_done = True
                            break

                # print('hey')
                self.clock.tick(60)
                pygame.display.update()

            except pygame.error:
                sys.exit()

    def level_run(self):
        try:
            while (not self.loaded_level.end_level and not self.loaded_level.game_over) \
                    or not self.loaded_level.finished_timer:

                for event_ in pygame.event.get():
                    if event_.type == pygame.QUIT:
                        self.save_to_file()
                        pygame.quit()
                        sys.exit(0)

                    elif event_.type == pygame.MOUSEBUTTONDOWN:
                        self.loaded_level.mouse_clicked = True

                self.loaded_level.draw()

                if self.is_crt:
                    self.display_crt()

                self.loaded_level.update()
                self.loaded_level.check()

                # print(self.loaded_level.current_timing)

                self.clock.tick(60)
                pygame.display.flip()
        except pygame.error:
            sys.exit()

    def reset(self):
        if self.counter > self.current_level:
            self.current_level = self.counter
        self.level_panel.update(self.current_level)
        self.menu.reset()
        self.score = 0
        self.hp = 0
        self.level_panel.reset()
        self.is_ready = True
        self.game_done = False
        self.is_choosing_level = False
        self.chosen_level = None
        self.is_viewing_high_score = False
        self.sound_controller.play_music()

    def display_util(self):
        self.screen.fill((30, 30, 30))
        self.gif_background.draw()
        if self.is_crt:
            self.display_crt()
        if self.is_ready:
            self.menu.show()
        elif self.is_loading:
            self.loading_panel.draw(self.screen)
        elif self.is_choosing_level:
            self.level_panel.show()
        elif self.game_done:
            if self.counter == self.max_level:
                display_ingame_text(self.screen, self.font,
                                    f'you"ve cleared all {self.max_level} levels',
                                    self.screen_width / 2, self.screen_height / 2 - 100, 0.8, 0.8)
                display_ingame_text(self.screen, self.font, f'end of journey for now',
                                    self.screen_width / 2, self.screen_height / 2 - 30, 0.8, 0.8)
                display_ingame_text(self.screen, self.font, f'to be continued...',
                                    self.screen_width / 2, self.screen_height / 2 + 40)
            elif self.loaded_level.save_level:
                display_ingame_text(self.screen, self.font, f'SAVED LEVEL',
                                    self.screen_width / 2, self.screen_height / 2 - 100, 1.4, 1.4)
                display_ingame_text(self.screen, self.font, f'you"ve passed {self.counter - self.chosen_level} '
                                                            f'levels, from level {self.chosen_level}',
                                    self.screen_width / 2, self.screen_height / 2 - 20, 0.8, 0.8)
            else:
                display_ingame_text(self.screen, self.font, f'Game over',
                                    self.screen_width / 2, self.screen_height / 2 - 100, 1.2, 1.2)
                display_ingame_text(self.screen, self.font, f'you"ve passed {self.counter - self.chosen_level} '
                                                            f'levels, from level {self.chosen_level}',
                                    self.screen_width / 2, self.screen_height / 2 - 20, 0.8, 0.8)
            display_ingame_text(self.screen, self.font, f'Press enter to exit',
                                self.screen_width / 2, self.screen_height / 2 + 200)

    def display_crt(self):
        self.crt.set_alpha(random.randint(150, 170))

        line_height = 2
        line_amount = int(self.screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.crt, 'black', (0, y_pos), (self.screen_width, y_pos), 1)

        self.screen.blit(self.crt, (-10, -10))

    def save_to_file(self):
        # pass
        self.save_info()
        print(self.saved_level)
        with open(resource_path('level.txt'), 'wb') as file:
            file.write(self.key.encrypt(json.dumps(self.saved_level, cls=ComplexEncoder, indent=4).encode()))

        if self.counter == 0:
            self.counter = 1
        if self.counter > self.current_level:
            counter = self.counter
        else:
            counter = self.current_level
        with open(resource_path(self.file_name), 'wb') as file:
            print(f'{int(self.coins)},{counter},,,,,\n')
            s = (f'{int(self.coins)},{counter},\n' +
                 '\n'.join(f'''\n{rng.StringGenerator().get(1000, 1, 1).split('_')}'''))
            s = self.key.encrypt(s.encode())

            file.write(s)

    def save_info(self):
        if self.loaded_level is not None:
            self.score = self.loaded_level.score
            self.coins = self.loaded_level.coins
            self.hp = self.loaded_level.player_health

    def check_saved_level(self):
        pack = [self.display, self.screen_width, self.screen_height, self.player,
                self.clock, self.sound_controller, self.font, random.choice(self.tips)]

        for i in range(1, self.max_level + 1):
            if len(self.presaved_level[i - 1]) != 0:
                loaded_level = self.levels[i - 1](*pack, f'level {i}', self.coins, self.score, self.hp)
                for name, val in self.presaved_level[i - 1].items():
                    if val is not None:
                        loaded_level.__setattr__(name, val)
                armies = []
                for enemies in self.presaved_level[i - 1]['enemies']:  # each enemy army
                    if enemies['enemy_amount'] != 0:
                        enemies_packs = []
                        for enemy_pack in enemies['enemy_packs']:  # each enemy row
                            enemy = []
                            for pack_dict in enemy_pack:  # each dict = enemy_col
                                if pack_dict is not None:
                                    enemy.append(Enemy(pack_dict['color'],
                                                       pack_dict['sp']['x'],
                                                       pack_dict['sp']['y'],
                                                       pack_dict['hp'],
                                                       pack_dict['dmg'],
                                                       pack_dict['score'],
                                                       pack_dict['cooldown'],
                                                       pack_dict['mlee_time']
                                                       ))
                                    enemy[len(enemy) - 1].check_ani()
                                    pack_dict.pop('ani')
                                    pack_dict.pop('normal_ani')
                                    pack_dict.pop('sp')
                                    for name, val in pack_dict.items():
                                        if val is not None:
                                            enemy[len(enemy) - 1].__setattr__(name, val)
                                else:
                                    enemy.append(None)
                            enemies_packs.append(enemy)
                        army = EnemyArmy(enemies_packs,
                                         enemies['enemy_amount'])
                        for name, val in enemies.items():
                            if val is not None and name != 'enemy_packs':
                                army.__setattr__(name, val)
                        armies.append(army)

                loaded_level.enemies = armies
                if loaded_level.level_code == 'boss':
                    loaded_level.recover()
                self.saved_level[i - 1] = loaded_level


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
