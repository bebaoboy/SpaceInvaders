import source.level as level
import source.enemy_deploy as deploy


class Level6(level.Level):
    def __init__(self, *pack):
        super().__init__(*pack)
        self.intro = 'classic invasion #3'
        colors = 'y'
        enemies = deploy.enemy_grid_deploy(cols=12, rows=11, colors=colors, initial_y=-20, initial_x=20)
        enemies.enemy_y_speed_countdown = 1000
        for enemy_row in enemies.enemy_packs:
            for enemy_col in enemy_row:
                enemy_col.hp = enemy_col.max_hp = 290
                enemy_col.dmg = 10
        self.append_enemy(enemies)
        self.laser_speed = -18
        self.laser_countdown = 200
        self.laser_type = 3
        self.equipment_type = 6
        self.laser_dmg = 62
        self.laser_speed_score += 600
        self.extra_enemy_health = 200
        self.extra_enemy_bonus = 200
        self.min_space_between = self.screen_width - 30
        self.max_space_between = self.screen_width

        self.max_waves = 2

        self.blocks.clear()
        self.make_multiple_blocks(max_space_between=self.max_space_between, min_space_between=self.min_space_between)
        for block_ in self.blocks:
            for blocks in block_.sprites():
                if blocks.rect.centerx > self.screen_width / 2:
                    blocks.__setattr__('x_speed', -1)
                else:
                    blocks.__setattr__('x_speed', 2)

        enemies = \
            deploy.enemy_row_deploy(cols=12, colors='r',
                                    initial_y=0, initial_x=900, x_speed=1, y_speed=0)
        enemies.enemy_laser_speed = 18
        enemies.enemy_shoot_cooldown = 10
        for enemy_row in enemies.enemy_packs:
            for enemy_col in enemy_row:
                enemy_col.hp = enemy_col.max_hp = 5000
                enemy_col.dmg = 10
        self.append_enemy(enemies)

    def special(self):
        # dif = self.current_timing - self.spawn_timer

        # timer
        # if dif < 8000 and self.enemies[len(self.enemies)-1].enemy_amount == 0:
        #     self.end_level = True

        # if dif >= 8000 and self.spawned_waves == 1:
        #     enemies = deploy.enemy_row_deploy(cols=5, colors='g', initial_y=220)
        #     enemies.enemy_y_speed_countdown = 2000
        #     self.append_enemy(enemies)

        self.moving_blocks()
