from random import randint
import math

import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, current_time, surf, pos,
                 constraint_x_left, constraint_x_right, constraint_y_down, constraint_y_up, dmg,
                 speed_y, speed_x=0.0, size_x=4, size_y=20, color='white' or (255, 255, 255, 255) or (255, 255, 255)):
        super().__init__()
        self.image = surf
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=pos)

        self.speed_x = speed_x
        self.speed_y = speed_y
        self.height_y_upper_constraint = constraint_y_up
        self.height_y_lower_constraint = constraint_y_down
        self.width_x_left_constraint = constraint_x_left
        self.width_x_right_constraint = constraint_x_right
        self.dmg = dmg
        self.time_to_live = 6000
        self.timer = current_time

        self.laser_list = []
        self.laser_queue = []

    def update(self, current_time):
        self.rect.centery += self.speed_y
        self.rect.centerx += self.speed_x
        self.laser_list.clear()
        self.destroy(current_time)

    def destroy(self, current_time):
        if current_time - self.timer >= self.time_to_live \
                or self.rect.centery < 0 \
                or self.rect.centery < self.height_y_lower_constraint \
                or self.rect.centery > self.height_y_upper_constraint \
                or self.rect.centerx < self.width_x_left_constraint \
                or self.rect.centerx > self.width_x_right_constraint:
            self.kill()

    def evaporate(self):
        pass


class SplitLaser(Laser):
    def __init__(self, current_time, surf, laser_list, time_to_split, pos,
                 constraint_x_left, constraint_x_right, constraint_y_down, constraint_y_up, dmg,
                 speed_y, speed_x=0.0, size_x=4, size_y=10, color='white'):
        super().__init__(current_time, surf, pos,
                         constraint_x_left, constraint_x_right, constraint_y_down, constraint_y_up, dmg,
                         speed_y, speed_x=speed_x, size_x=size_x, size_y=size_y, color=color)

        self.laser_queue: list = laser_list  # later to put on laser list
        self.time_to_split = time_to_split
        self.split_timer = current_time

    def update(self, current_time):
        super().update(current_time)
        if self.time_to_split is not None and current_time - self.split_timer >= self.time_to_split:
            for laser_ in self.laser_queue:
                laser_.rect.centery = self.rect.centery
                laser_.rect.centerx = self.rect.centerx
            self.laser_list.extend(self.laser_queue)
            self.timer = -5000
            self.time_to_split = None


class GatlingLaser(Laser):
    def __init__(self, current_time, surf, laser_list, time_span, pos,
                 constraint_x_left, constraint_x_right, constraint_y_down, constraint_y_up, dmg,
                 speed_y, speed_x=0.0, size_x=0, size_y=0, color='white'):
        super().__init__(current_time, surf, pos,
                         constraint_x_left, constraint_x_right, constraint_y_down, constraint_y_up, dmg,
                         speed_y, speed_x=speed_x, size_x=size_x, size_y=size_y, color=color)
        self.laser_queue = laser_list
        self.time_span: list = time_span
        assert (len(self.laser_queue) == len(self.time_span))
        self.gatling_timer = current_time
        self.is_fired = [False] * len(self.time_span)
        self.idx = 0

    def update(self, current_time):
        super(GatlingLaser, self).update(current_time)
        if self.idx < len(self.time_span) \
                and not self.is_fired[self.idx] \
                and current_time - self.gatling_timer >= self.time_span[self.idx]:
            if type(self.laser_queue[self.idx]) is not list:
                self.laser_queue[self.idx].time_to_live *= 1.5
                self.laser_list.append(self.laser_queue[self.idx])
            else:
                for laser_ in self.laser_queue[self.idx]:
                    laser_.time_to_live *= 1.5
                self.laser_list.extend(self.laser_queue[self.idx])
            # print(f'idx={self.idx}, {current_time - self.gatling_timer}')
            self.gatling_timer = current_time
            self.is_fired[self.idx] = True
            self.idx += 1


class BouncyLaser(Laser):
    def __init__(self, current_time, surf, pos,
                 constraint_x_left, constraint_x_right, constraint_y_down, constraint_y_up, dmg,
                 speed_y, speed_x=0.0, size_x=4, size_y=20, color='white', eva=0.8):
        super().__init__(current_time, surf, pos,
                         constraint_x_left, constraint_x_right, constraint_y_down, constraint_y_up, dmg,
                         speed_y, speed_x=speed_x, size_x=size_x, size_y=size_y, color=color)
        self.time_to_live *= 1.5
        self.evaporate_speed = eva

    def update(self, current_time):
        super(BouncyLaser, self).update(current_time)
        self.rect.centery += self.speed_y
        self.rect.centerx += self.speed_x
        self.laser_list.clear()
        if (self.rect.centerx >= self.width_x_right_constraint) \
                and self.speed_x > 0.0:
            self.speed_x = -abs(self.speed_x)
            self.evaporate()

        elif (self.rect.centerx <= self.width_x_left_constraint) \
                and self.speed_x < 0.0:
            self.speed_x = abs(self.speed_x)
            self.evaporate()

        if self.rect.bottom >= self.height_y_upper_constraint \
                and self.speed_y > 0.0:
            self.speed_y = -abs(self.speed_y)
            self.evaporate()

        elif self.rect.top <= self.height_y_lower_constraint \
                and self.speed_y < 0.0:
            self.speed_y = abs(self.speed_y)
            self.evaporate()
            
    def evaporate(self):
        self.dmg *= self.evaporate_speed
        self.time_to_live *= self.evaporate_speed


def get_player_laser(types: str or int, rec, current_time, surf, dmg, laser_speed,
                     screen_width=0, screen_height=0, color='white'):
    lasers_list = []
    if types == 1:
        lasers_list.append(Laser(current_time, surf, rec.midtop, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, color=color))
    elif types == 2:
        lasers_list.append(Laser(current_time, surf, rec.topleft, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, color=color))
        lasers_list.append(Laser(current_time, surf, rec.topright, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, color=color))
    elif types == 3:
        lasers_list.append(Laser(current_time, surf, rec.midleft, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, color=color))
        lasers_list.append(Laser(current_time, surf, rec.midtop, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, color=color))
        lasers_list.append(Laser(current_time, surf, rec.midright, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, color=color))
    elif types == 4:
        lasers_list.append(Laser(current_time, surf, rec.midleft, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, color=color))
        lasers_list.append(Laser(current_time, surf, rec.midleft, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, laser_speed / 4))
        lasers_list.append(Laser(current_time, surf, rec.midright, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, -laser_speed / 4))
        lasers_list.append(Laser(current_time, surf, rec.midright, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, color=color))
    elif types == 5:
        lasers_list.append(Laser(current_time, surf, rec.midleft, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, color=color))
        lasers_list.append(Laser(current_time, surf, rec.midleft, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, laser_speed / 5))
        lasers_list.append(Laser(current_time, surf, rec.midright, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, -laser_speed / 5))
        lasers_list.append(Laser(current_time, surf, rec.midright, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, color=color))
        lasers_list.append(Laser(current_time, surf, rec.topright, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, -laser_speed / 4))
        lasers_list.append(Laser(current_time, surf, rec.topleft, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, laser_speed / 4))
    elif types == 6:
        lasers_list.append(Laser(current_time, surf, rec.midleft, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, color='yellow'))
        lasers_list.append(Laser(current_time, surf, rec.midright, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed, color='yellow'))
        lasers_list.append(Laser(current_time, surf, rec.midleft, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed * 0.8))
        lasers_list.append(Laser(current_time, surf, rec.midright, 0, screen_width, 0,
                                 rec.bottom, dmg, laser_speed * 0.8))
        lasers_list.append(Laser(current_time, surf, (rec.left - 15, rec.bottomleft[1] + 25), 0, screen_width, 0,
                                 rec.bottom + 26, dmg, laser_speed, color='yellow'))
        lasers_list.append(Laser(current_time, surf, (rec.right + 15, rec.bottomright[1] + 25), 0, screen_width, 0,
                                 rec.bottom + 26, dmg, laser_speed, color='yellow'))

    elif types == 'r':
        lasers_list.append(Laser(current_time, surf,
                                 rec.center,
                                 0, screen_width, 0, screen_height,
                                 dmg,
                                 laser_speed))
    elif types == 'b':
        lasers_list.append(Laser(current_time, surf,
                                 rec.midleft,
                                 0, screen_width, 0, screen_height,
                                 dmg,
                                 laser_speed + 1, speed_x=-2, color='light blue'))

        lasers_list.append(Laser(current_time, surf,
                                 rec.midright,
                                 0, screen_width, 0, screen_height,
                                 dmg,
                                 laser_speed + 1, speed_x=2, color='light blue'))

        lasers_list.append(Laser(current_time, surf,
                                 rec.center,
                                 0, screen_width, 0, screen_height,
                                 dmg,
                                 laser_speed + 1, color='light blue'))

    elif types == 'y':
        direction = randint(0, 2)
        if direction == 0:
            for _ in range(10, 50):
                lasers_list.append(Laser(current_time, surf,
                                         rec.midright,
                                         0, screen_width,
                                         rec.top - 200,
                                         rec.bottom + 600,
                                         dmg,
                                         min(13.0, laser_speed + 0.5), speed_x=-20 + _))
        else:
            if rec.top > screen_width:
                for _ in range(-10, 11):
                    li = Laser(current_time, surf,
                               rec.midleft,
                               rec.left - 550,
                               rec.right + 550,
                               rec.top - 300,
                               rec.bottom + 600,
                               dmg,
                               laser_speed / 5 + _, speed_x=-(0.2 + 7 / 5))
                    li.time_to_live = 5500
                    lasers_list.append(li)
            else:
                for _ in range(-10, 11):
                    li = Laser(current_time, surf,
                               rec.midright,
                               rec.left - 550,
                               rec.right + 550,
                               rec.top - 300,
                               rec.bottom + 600,
                               dmg,
                               laser_speed / 5 + _, speed_x=(0.2 + 7 / 5))
                    li.time_to_live = 5500
                    lasers_list.append(li)

    elif types == 'g':
        theta = 0
        x = rec.centerx
        y = rec.centery
        step = 30

        while theta < 360:
            lasers_list.append(Laser(current_time, surf,
                                     rec.midtop,
                                     rec.left - 250,
                                     rec.right + 250,
                                     rec.top - 200,
                                     rec.bottom + 600,
                                     dmg,
                                     min(8, 0.01 * y * math.sin(theta)), 0.01 * x * math.cos(theta), size_x=7,
                                     size_y=7))
            theta += step

    elif types == 'y_boss':
        theta = 0
        x = rec.centerx
        y = rec.centery
        step = 30

        while theta < 360:
            lasers_list.append(Laser(current_time, surf,
                                     rec.midtop,
                                     rec.left - 550,
                                     rec.right + 550,
                                     rec.top - 200,
                                     rec.bottom + 600,
                                     dmg,
                                     min(8, 0.01 * y * math.sin(theta)), 0.01 * x * math.cos(theta)))
            theta += step

        for _ in range(10, 20):
            lasers_list.append(Laser(current_time, surf,
                                     rec.midright,
                                     0, screen_width,
                                     rec.top - 200,
                                     rec.bottom + 600,
                                     dmg + 75,
                                     min(13.0, laser_speed + 0.5), speed_x=-20 + _, color='red'))
        for _ in range(10, 30):
            lasers_list.append(Laser(current_time, surf,
                                     (rec.midleft[0], rec.midleft[1] - 70),
                                     0, screen_width,
                                     rec.top - 200,
                                     rec.bottom + 600,
                                     dmg * 0.85,
                                     min(13.0, laser_speed + 0.5), speed_x=-20 + _, color='yellow'))

    elif types == 'r_bouncy':
        lasers_list.append(BouncyLaser(current_time, surf,
                                       rec.center,
                                       0, screen_width, 0, screen_height,
                                       dmg,
                                       laser_speed))

    elif types.startswith('b_split_bouncy'):
        lasers_list.append(SplitLaser(current_time, surf, [
            BouncyLaser(current_time, surf,
                        rec.center,
                        0, screen_width, 0, screen_height,
                        dmg / 2,
                        laser_speed - 1, speed_x=1, color='blue'),
            BouncyLaser(current_time, surf,
                        rec.center,
                        0, screen_width, 0, screen_height,
                        dmg / 2,
                        laser_speed - 1, speed_x=-1, color='blue')
        ],
                                      500,
                                      rec.midleft,
                                      0, screen_width, 0, screen_height,
                                      dmg,
                                      laser_speed - 1, speed_x=-2, color='light blue'))

        lasers_list.append(SplitLaser(current_time, surf, [
            BouncyLaser(current_time, surf,
                        rec.center,
                        0, screen_width, 0, screen_height,
                        dmg / 2,
                        laser_speed - 1, speed_x=1, color='blue'),
            BouncyLaser(current_time, surf,
                        rec.center,
                        0, screen_width, 0, screen_height,
                        dmg / 2,
                        laser_speed - 1, speed_x=-1, color='blue')
        ],
                                      500,
                                      rec.midright,
                                      0, screen_width, 0, screen_height,
                                      dmg,
                                      laser_speed - 1, speed_x=2, color='light blue'))

        lasers_list.append(Laser(current_time, surf,
                                 rec.center,
                                 0, screen_width, 0, screen_height,
                                 dmg,
                                 laser_speed, color='light blue'))

        if types.endswith('raining'):
            for laser_ in lasers_list:
                for laser__ in laser_.laser_queue:
                    laser__.time_to_live *= 1.1

    elif types == 'b_boss_rotate':
        theta = 0
        x = rec.centerx
        y = rec.centery
        step = 20

        while theta < 360:
            lasers_list.append(BouncyLaser(current_time, surf,
                                           rec.center,
                                           rec.left - 250,
                                           rec.right + 250,
                                           rec.top - 200,
                                           rec.bottom + 600,
                                           dmg * 0.8,
                                           min(8, 0.01 * y * math.sin(theta)) + 1, 0.01 * x * math.cos(theta) + 1,
                                           size_x=20, size_y=7, eva=1,
                                           color='blue'))
            theta += step

    elif types == 'p':
        lasers_list.append(GatlingLaser(current_time, surf,
                                        [
                                            Laser(current_time, surf, rec.center,
                                                  0, screen_width, 0, screen_height,
                                                  dmg, laser_speed, color=(240, 0, 255, 128)),
                                            [
                                                Laser(current_time, surf, rec.topleft, 0, screen_width, 0,
                                                      screen_height,
                                                      dmg, laser_speed, color=(240, 0, 255, 128)),
                                                Laser(current_time, surf, rec.topright, 0, screen_width, 0,
                                                      screen_height,
                                                      dmg, laser_speed, color=(240, 0, 255, 128))
                                            ],
                                            [
                                                Laser(current_time, surf, rec.center, 0, screen_width, 0, screen_height,
                                                      dmg, laser_speed, color=(240, 0, 255, 128)),
                                                Laser(current_time, surf, rec.topleft, 0, screen_width, 0,
                                                      screen_height,
                                                      dmg, laser_speed, color=(240, 0, 255, 128)),
                                                Laser(current_time, surf, rec.topright, 0, screen_width, 0,
                                                      screen_height,
                                                      dmg, laser_speed, color=(240, 0, 255, 128))
                                            ]
                                        ],
                                        [
                                            500, 500, 500
                                        ],
                                        rec.center,
                                        0, screen_width, 0, screen_height,
                                        dmg,
                                        laser_speed
                                        ))

    elif types == 'p_gatling':
        theta = 0
        x = rec.centerx
        y = rec.centery
        step = 30
        laser_list = []

        while theta < 360:
            laser_list.append(Laser(current_time, surf,
                                    rec.midtop,
                                    rec.left - 300,
                                    rec.right + 300,
                                    rec.top - 200,
                                    rec.bottom + 700,
                                    dmg,
                                    max(6, 0.01 * y * math.sin(theta)), 0.005 * x * math.cos(theta) + 0.1,
                                    color=(240, 0, 255, 128)))
            theta += step
        lasers_list.append(GatlingLaser(current_time, surf,
                                        laser_list,
                                        [100] * len(laser_list),
                                        rec.center,
                                        0, screen_width, 0, screen_height,
                                        dmg,
                                        laser_speed
                                        ))

    elif types.startswith('o'):
        lasers_list.append(SplitLaser(current_time, surf, [
            BouncyLaser(current_time, surf,
                        rec.center,
                        0, screen_width, 0, screen_height,
                        dmg / 2,
                        laser_speed, speed_x=0, color=(255, 100, 10), size_x=10, size_y=8),
            Laser(current_time, surf,
                  rec.center,
                  0, screen_width, 0, screen_height,
                  dmg / 2,
                  laser_speed, speed_x=-2, color=(255, 100, 10), size_x=10, size_y=8)
        ],
                                      500,
                                      rec.midleft,
                                      0, screen_width, 0, screen_height,
                                      dmg,
                                      laser_speed, speed_x=-2, color=(255, 100, 10)))

        lasers_list.append(SplitLaser(current_time, surf, [
            BouncyLaser(current_time, surf,
                        rec.center,
                        0, screen_width, 0, screen_height,
                        dmg / 2,
                        laser_speed, speed_x=2, color=(255, 100, 10), size_x=10, size_y=8),
            Laser(current_time, surf,
                  rec.center,
                  0, screen_width, 0, screen_height,
                  dmg / 2,
                  laser_speed, speed_x=0, color=(255, 100, 10), size_x=10, size_y=8)
        ],
                                      500,
                                      rec.midright,
                                      0, screen_width, 0, screen_height,
                                      dmg,
                                      laser_speed, speed_x=2, color=(255, 100, 10)))

        lasers_list.append(Laser(current_time, surf,
                                 rec.center,
                                 0, screen_width, 0, screen_height,
                                 dmg,
                                 laser_speed + 1, color=(255, 100, 10), size_x=15, size_y=10))

    return lasers_list
