import source.level as level
import source.enemy_deploy as deploy


class Level17(level.Level):
    def __init__(self, *pack):
        super().__init__(*pack)

        self.intro = 'orange is easily shattered'

        colors = [
            [''] * 3 + ['o'] + [''] * 3,
            [''] * 2 + ['o'] + [''] + ['o'] + [''] * 2,
            [''] * 2 + ['o'] * 3 + [''] * 2,
            [''] * 1 + ['o'] * 5 + [''] * 1,
            ['o'] * 7,
        ]
        enemies = deploy.enemy_grid_deploy(cols=7, rows=5, colors=colors, initial_y=10, initial_x=200, x_speed=2,
                                           y_speed=1)
        enemies.enemy_y_lower_constraint = -20
        enemies.enemy_y_upper_constraint = 300
        enemies.enemy_laser_speed = 10

        enemies.enemy_shoot_cooldown = 20
        enemies.enemy_y_speed_countdown = 0

        enemies.enemy_shoot_cooldown = 700
        self.append_enemy(enemies)

        self.laser_type = 3
        self.laser_dmg = 10
        self.laser_countdown = 500

        self.blocks.clear()
        self.max_space_between = self.screen_width / 2 + 1
        self.min_space_between = self.screen_width / 2 - 10
        self.make_multiple_blocks(max_space_between=self.max_space_between, min_space_between=self.min_space_between)
