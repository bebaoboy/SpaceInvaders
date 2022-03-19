import random

from source import block
from source.level import Level
from source.display_ingame_text import display_ingame_text


class S_Level(Level):
    def __init__(self, *pack):
        super(S_Level, self).__init__(*pack)

        # special variable goes here
        # self.logo = ...

        self.level_code = ''


class BossLevel(S_Level):
    def __init__(self, *pack):
        super(S_Level, self).__init__(*pack)

        # special variable goes here
        # self.logo = ...
        self.intro = 'SHOW EM WHO"S BOSS'
        self.level_code = 'boss'

    def recover(self):
        pass


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
