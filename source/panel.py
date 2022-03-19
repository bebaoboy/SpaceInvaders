import pygame

from source.resource_path import resource_path
from source.button import Button


class PauseButton(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(PauseButton, self).__init__()
        self.image = pygame.image.load(resource_path('graphics/pause.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect(topleft=pos)


class PausePanel:
    def __init__(self, screen, font, size_x=500, size_y=400):
        self.screen = screen
        self.size_x = size_x
        self.size_y = size_y
        self.panel = pygame.surface.Surface((self.size_x, self.size_y))
        self.panel.fill('black')
        self.rect = pygame.Rect(200, 150, self.size_x, self.size_y)
        self.font = font

        x_scale = y_scale = 0.8
        self.title = self.font.render('PAUSE', True, 'white')
        self.title = pygame.transform.scale(
            self.title, (self.title.get_width() * x_scale, self.title.get_height() * y_scale))

        self.panel.blit(self.title, self.title.get_rect(center=(self.size_x / 2, 30)))

        self.title = self.font.render('Click outside to unpause'.upper(), True, 'white')
        self.title = pygame.transform.scale(
            self.title, (self.title.get_width() * x_scale, self.title.get_height() * y_scale))
        self.panel.blit(self.title, self.title.get_rect(center=(self.size_x / 2, self.size_y - 40)))

        self.quit_prompt = Button(self.font, 30, self.screen, 'Press to quit'.upper(),
                                  (self.size_x / 2 - 120 + 200, self.size_y / 2 + 100), (0, 0, 0),
                                  feedback='SAVE THE GAME?'.upper())
        self.quit_prompt.blit_button()

        self.quit_button = Button(self.font, 30, self.screen, 'QUIT'.upper(),
                                  (self.size_x / 2 - 170 + 200, self.size_y / 2 + 180), (0, 0, 0))
        self.quit_button.blit_button()

        self.save_button = Button(self.font, 30, self.screen, 'SAVE'.upper(),
                                  (self.size_x / 2 + 200 + 90, self.size_y / 2 + 180), (0, 0, 0))
        self.save_button.blit_button()
        self.pending = False
        self.pending_timer = 0

    def draw(self):
        self.screen.blit(self.panel, self.rect)
        self.quit_prompt.show()
        if self.pending:
            self.quit_button.show()
            self.save_button.show()

    def clicked(self, current_timing):
        # if (self.current_timing - self.pending_timer >= 3000 or not self.pending) and self.quit_prompt.clicked():
        #     if not self.pending:
        #         self.pending = True
        #         self.pending_timer = self.current_timing
        #     else:
        #         return True
        if not self.pending:
            if self.quit_prompt.clicked():
                self.pending = True
                self.pending_timer = current_timing
        else:
            if current_timing - self.pending_timer >= 1000:
                if self.quit_button.clicked():
                    return -1
                elif self.save_button.clicked():
                    return 1

        if current_timing - self.pending_timer >= 6000:
            self.reset()
            self.pending_timer = current_timing

        return False

    def reset(self):
        self.quit_prompt.reset()
        self.quit_button.reset()
        self.save_button.reset()
        self.pending = False


class LoadingPanel:
    def __init__(self, font, size_x=400, size_y=200):
        self.size_x = size_x
        self.size_y = size_y
        self.panel = pygame.surface.Surface((self.size_x, self.size_y))
        self.panel.fill('black')
        self.rect = pygame.Rect(250, 250, self.size_x, self.size_y)
        self.font = font

        x_scale = y_scale = 0.8
        self.title = self.font.render('LOADING', True, 'white')
        self.title = pygame.transform.scale(
            self.title, (self.title.get_width() * x_scale, self.title.get_height() * y_scale))

        self.panel.blit(self.title, self.title.get_rect(center=(self.size_x / 2, self.size_y / 2)))

    def draw(self, screen):
        screen.blit(self.panel, self.rect)
