import pygame

shape = [
    '    xxxxxxx',
    '   xxxxxxxxx',
    '  xxxxxxxxxxx',
    ' xxxxxxxxxxxxx',
    'xxxxxxxxxxxxxxx',
    'xxxxxxxxxxxxxxxx',
    'xxxxxxxxxxxxxxxx',
    'xxxx        xxxx',
    'xxx          xxx'
]

# raining_shape = [
#     '    xxxxxxxxxxxxxxxx',
#     '    xxxxxxxxxxxxxxxx',
#     '   xxxxxxxxxxxxxxxxxx',
#     '  xxxxxxxxxxxxxxxxxxxx',
#     ' xxxxxxxxxxxxxxxxxxxxxx',
#     'xxxxxxxxxxxxxxxxxxxxxxxx',
#     'xxxxxxxxxxxxxxxxxxxxxxxx',
#     'xxxxxxxxxxxxxxxxxxxxxxxx',
#     'xxx                  xxx'
# ]

raining_shape = [
    '            xxxx',
    '          xxxxxxxx',
    '        xxxxxxxxxxxx',
    '     xxxxxxxxxxxxxxxxxx',
    '    xxxxxxxxxxxxxxxxxxxx',
    '    xxxxxxxxxxxxxxxxxxxx',
    '  xxxxxxxxxxxxxxxxxxxxxxxxx',
    '  xxxxxxxxxxxxxxxxxxxxxxxxx',
    'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'xxx          xx           xxx',
    '             xx              ',
    '             xx              '
]

player_shape = [
    '         xxx',
    '    xxxxxxxxxxxxxx',
    '  xxxxxxxxxxxxxxxxxx',
    '  xxxxxxx    xxxxxxx',
    'xxxxxxxxx    xxxxxxxxx',
    'xxxxxxxxxxxxxxxxxxxxxx'
]


class Block(pygame.sprite.Sprite):
    def __init__(self, color, size, x, y, x_speed=0, y_speed=0):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed
        # if self.rect.centerx < x_left_constraint:
        #     self.rect.centerx = x_left_constraint + 2
        #     self.x_speed = abs(self.x_speed)
        # elif self.rect.centerx > x_right_constraint:
        #     self.rect.centerx = x_right_constraint - 2
        #     self.x_speed = -abs(self.x_speed)
        # if self.rect.top < y_upper_constraint:
        #     self.rect.centery = y_upper_constraint + 2
        #     self.y_speed = abs(self.y_speed)
        # elif self.rect.bottom > y_lower_constraint:
        #     self.rect.centery = y_lower_constraint - 2
        #     self.y_speed = -abs(self.y_speed)
