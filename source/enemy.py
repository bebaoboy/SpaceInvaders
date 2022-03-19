import pygame

from source import game
import source.resource_manager as resource_manager


class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()

        self.image = resource_manager.enemy_pic[color.split('_')[0]]
        self.image = pygame.transform.scale(
            self.image, (self.image.get_rect().width * 1.2, self.image.get_rect().height * 1.3))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x_speed, y_speed):
        self.rect.x += x_speed
        self.rect.y += y_speed


class Enemy:
    def __init__(self, color='b', x=0, y=0, hp=50, dmg=50, score=15, cooldown=3000, mlee=5000, ani_change=900):
        self.sp = pygame.sprite.GroupSingle(EnemySprite(color, x, y))
        self.color = color
        self.timer = 0
        self.max_hp = hp
        self.hp = hp
        self.dmg = dmg
        self.mlee_dmg = max(hp / dmg * 2, 150)
        self.score = score
        self.mlee_timer = 0
        self.mleed = False
        self.cooldown = cooldown
        self.mlee_time = mlee

        self.another_img = None
        self.another_rect = None

        self.normal_ani = self.sp.sprite.image
        self.ani_timer = 0
        self.ani_change = ani_change

        self.rotate_angle = 0
        self.rotate_speed = .2
        self.rotate_timer = 0
        self.rotate_countdown = None
        self.ani = None
        self.check_ani()

    def check_ani(self):
        try:
            ani_path = resource_manager.resource_path('graphics/' + self.color.split('_')[0] + '_ani.png')
            self.ani = pygame.image.load(ani_path).convert_alpha()
            self.ani = pygame.transform.scale(
                self.ani, (self.ani.get_rect().width * 1.2, self.ani.get_rect().height * 1.3))
        except (Exception,):
            self.ani = None

    def update(self, current_timing, x_speed, y_speed):
        self.sp.update(x_speed, y_speed)

        if self.ani is not None and current_timing - self.ani_timer >= self.ani_change:
            if self.sp.sprite.image == self.normal_ani:
                self.sp.sprite.image = self.ani
            else:
                self.sp.sprite.image = self.normal_ani

            self.ani_timer = current_timing

        if self.rotate_countdown is not None:
            if current_timing - self.rotate_timer >= self.rotate_countdown:
                self.rotate()
                # print('rot')
                self.rotate_timer = current_timing

    def rotate(self):
        self.rotate_angle = (self.rotate_angle + self.rotate_speed) % 360
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotozoom(self.sp.sprite.image, self.rotate_angle, 1)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=self.sp.sprite.rect.center)
        self.another_img = new_image
        self.another_rect = rect

    def reprJSON(self):
        self.another_img = None
        self.another_rect = None
        dick = self.__dict__
        for name, val in dick.items():
            if name.find('timer') != -1:
                dick[name] = 0 - val
            if type(val) is pygame.surface.Surface:
                dick[name] = None
        dick['normal_ani'] = None
        dick['sp'] = dict(x=self.sp.sprite.rect.x, y=self.sp.sprite.rect.y)
        return dick


class EnemyArmy:
    def __init__(self, enemy_packs: list[list[Enemy]], amount,
                 x_speed=1, y_speed=1, y_speed_countdown=4000, shoot_countdown=500, laser_speed=8, drop_time=10):
        self.enemy_packs = enemy_packs

        self.enemy_shoot_cooldown = shoot_countdown
        self.enemy_laser_speed = laser_speed
        self.enemy_cooldown_timer = 0

        self.enemy_y_speed = y_speed
        self.enemy_y_timer = 0
        self.enemy_y_speed_countdown = y_speed_countdown
        self.enemy_move_down_already = False
        self.enemy_y_speed_drop_time = drop_time
        self.enemy_y_speed_drop_rate = 10

        self.enemy_x_speed = x_speed
        self.enemy_x_timer = 0
        self.enemy_x_speed_countdown = 0
        self.enemy_move_x_already = False
        self.enemy_x_speed_drop_time = 0
        self.enemy_x_speed_drop_rate = 1

        self.enemy_y_lower_constraint = None
        self.enemy_y_upper_constraint = None

        self.enemy_x_left_constraint = None
        self.enemy_x_right_constraint = None

        self.enemy_amount = amount

        # self.is_spawned = False

    def update(self, current_timing, x_speed, y_speed):
        for row_idx, enemy_row in enumerate(self.enemy_packs):
            for col_idx, enemy_col in enumerate(enemy_row):
                if enemy_col is not None:
                    enemy_col.update(current_timing, x_speed, y_speed)

    def kill(self, row_idx, col_idx: int):
        # noinspection PyTypeChecker
        self.enemy_packs[row_idx][col_idx] = None

    def reprJSON(self):
        dick = self.__dict__
        for name, val in dick.items():
            if name.find('timer') != -1:
                dick[name] = 0
            if type(val) is pygame.surface.Surface:
                dick[name] = None
        packs = [[None] * len(self.enemy_packs[0]) for _ in range(len(self.enemy_packs))]
        for row in range(len(self.enemy_packs)):
            for col in range(len(self.enemy_packs[0])):
                if self.enemy_packs[row][col] is not None:
                    packs[row][col] = self.enemy_packs[row][col].reprJSON()
        dick['enemy_packs'] = packs
        return dick


class ExtraEnemy(pygame.sprite.Sprite):
    def __init__(self, speed, side, screen_width, height, hp):
        super().__init__()
        self.image = pygame.image.load(game.resource_path('graphics/extra.png')).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.image.get_rect().width * 1.4, self.image.get_rect().height * 1.3))
        self.side = side
        self.hp = hp

        if side == 'right':
            x = screen_width + 50
            self.end = -300
        else:
            x = -50
            self.end = screen_width + 300

        self.speed = speed
        self.rect = self.image.get_rect(topleft=(x, height))

    def update(self):
        if (self.side == 'right' and self.rect.x <= self.end) \
                or (self.side == 'left' and self.rect.x >= self.end):
            self.kill()
            # print('DEADDDDDDDDDDDDDDDDDDDD')

        self.rect.x += self.speed
