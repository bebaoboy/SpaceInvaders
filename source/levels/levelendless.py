import random
from source.s_level import EndlessLevel


class EndlessLevelA(EndlessLevel):
    def __init__(self, *pack):
        super().__init__(*pack)

        self.intro = 'Enjoy.'

        self.laser_type = 4
        self.laser_speed = -15
        self.laser_countdown = 500
        self.laser_dmg = 70
        self.equipment_type = 3

        self.spawn_time = random.choice(self.spawn_time_list)

        self.max_space_between = 600
        self.min_space_between = 300
        self.blocks.clear()
        self.make_multiple_blocks(max_space_between=self.max_space_between, min_space_between=self.min_space_between)
