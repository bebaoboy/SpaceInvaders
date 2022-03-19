import source.button
from source import menu
import pygame

from source.resource_path import resource_path


class LevelGrid:
    def __init__(self, font, font_size, screen, width, height, min_level, max_level, current_level,
                 space=50, bg=(0, 0, 0, 0), color='white'):
        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        self.bg = bg
        self.space = space
        self.font = font
        self.font_size = font_size
        self.color = color
        self.inner_bg = (0, 245, 245, 100)

        self.min_level = min_level
        self.max_level = max_level
        self.current_level = current_level

        self.level_panel_title = source.button.Button(
            self.font, self.font_size + 20, self.screen, "Levels", (
                self.screen_width / 2 - 100, 50
            ), self.bg, text_pos=(15, 10)
        )

        self.level_panel_title.image = pygame.image.load(resource_path('graphics/r.png')).convert_alpha()
        self.level_panel_title.blit_button()

        self.level_row_x = 58
        self.level_row_y = 150
        self.x_space = 20
        self.y_space = 20

        self.level_cell = pygame.image.load(resource_path('graphics/level_square.png')).convert_alpha()
        self.level_cell = pygame.transform.scale(self.level_cell, (80, 80))
        self.level_cell_locked = pygame.image.load(resource_path('graphics/level_square_locked.png')).convert_alpha()
        self.level_cell_locked.set_alpha(50)
        self.level_cell_locked = pygame.transform.scale(self.level_cell_locked, (80, 80))

        self.level_grid = []
        x = self.level_row_x
        y = self.level_row_y

        level_cells = []

        for i in range(self.min_level, self.max_level + 1):
            if i <= self.current_level:
                img = self.level_cell
            else:
                img = self.level_cell_locked

            if i == current_level:
                inner_bg = self.inner_bg
            else:
                inner_bg = None
            level_cells.append(
                LevelCell(self.font, self.font_size + 10, self.screen, str(i), (x, y),
                          bg, img=img, inner_bg=inner_bg))
            x += self.level_cell.get_width() + self.x_space

            if i % 8 == 0:
                self.level_grid.append(level_cells)
                self.level_row_y += self.level_cell.get_height() + self.y_space
                y = self.level_row_y
                x = self.level_row_x

        for level_row in self.level_grid:
            for level in level_row:
                level.blit_button()

    def update(self, lv):
        self.current_level = lv
        for level_row in self.level_grid:
            for level in level_row:
                if int(level.original_text) < self.current_level:
                    level.inner_bg = None
                    level.image = self.level_cell
                elif int(level.original_text) > self.current_level:
                    level.inner_bg = None
                    level.image = self.level_cell_locked
                else:
                    level.inner_bg = self.inner_bg
                    level.image = self.level_cell

    def show(self):
        self.level_panel_title.show()
        for level_row in self.level_grid:
            for level in level_row:
                level.show()

    def reset(self):
        self.level_panel_title.reset()
        for level_row in self.level_grid:
            for level in level_row:
                level.reset()

    def clicked(self):
        for level_row in self.level_grid:
            for level in level_row:
                lv = int(level.original_text)
                if lv <= self.current_level and level.clicked():
                    if level.clicked():
                        return lv


class LevelCell(source.button.Button):
    def __init__(self, font, font_size, screen, text, pos, bg, feedback="", color='white', img=None, inner_bg=None):
        super(LevelCell, self).__init__(font, font_size, screen, text, pos, bg,
                                        feedback=feedback, color=color, img=img, inner_bg=None)
        self.text_pos = ((self.image.get_width() - self.text.get_width()) / 2,
                         (self.image.get_height() - self.text.get_height()) / 2)
        self.inner_bg = inner_bg

    def get_size_rect(self):
        return self.image.get_size()

    def fill_background(self):
        self.surface.fill(self.bg)
        if self.inner_bg is not None:
            x, y, w, h = self.image.get_rect()
            offset = 5
            self.surface.fill(self.inner_bg, (x + offset, y + offset, w - offset * 2, h - offset * 2))
