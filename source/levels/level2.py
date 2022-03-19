import source.level as level
import source.enemy_deploy as deploy


class Level2(level.Level):
    def __init__(self, *pack):
        super().__init__(*pack)

        self.intro = 'classic invasion #1'

        colors = [
                    ['g'] * 10,
                    ['y'] * 4 + ['b', 'r'] + ['y'] * 4,
                    ['b'] * 4 + ['r', 'b'] + ['y'] * 4,
                    ['b'] * 10,
                    ['r'] * 10
            ]
        enemies = deploy.enemy_grid_deploy(rows=5, cols=10, colors=colors, initial_y=200)
        self.append_enemy(enemies)

        self.laser_type = 4
        self.laser_countdown = self.laser_min_countdown + 300
