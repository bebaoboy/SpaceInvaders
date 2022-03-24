import source.level as level
import source.enemy_deploy as deploy


class Level3(level.Level):
    def __init__(self, *pack):
        super().__init__(*pack)
        self.intro = 'BEWARE!'
        self.intro_time = 1000

        colors = [
            ['r'] * 8,
            ['r'] * 8,
            ['y'] * 3 + ['b', 'r'] + ['g'] * 3,
            ['g', 'y', 'r', 'b', 'y'] + ['r'] * 3,
            ['y'] * 3 + ['r', 'b'] + ['y'] * 3,
            ['b'] * 8,
            ['g'] * 8,
            ['r'] * 8,
            ['y'] * 3 + ['b', 'r'] + ['g'] * 3,
            ['g', 'y', 'r', 'b', 'y'] + ['r'] * 3,
            ['y'] * 3 + ['r', 'b'] + ['y'] * 3,
            ['g'] * 8
        ]
        enemies = \
            deploy.enemy_grid_deploy(rows=12, cols=8, colors=colors, initial_y=50)
        enemies.enemy_shoot_cooldown = 100

        self.append_enemy(enemies)
        self.laser_countdown = 100
        self.laser_speed = -19
        self.laser_speed_score = 100 + self.player_health
        self.laser_type = 4
        self.blocks.clear()
        self.laser_dmg = 500

        self.end_level_hint = 'that was fun!'
