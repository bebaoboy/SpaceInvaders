import pygame


class Button:
    def __init__(self, font, font_size, screen, text, pos, bg, feedback="", color='white',
                 img=None, inner_bg=None, text_pos=(0, 0), img_pos=(0, 0)):
        self.x, self.y = pos

        # self.font = pygame.font.SysFont("Arial", font)
        if type(font) is not str:
            self.font = font
        else:
            self.font = pygame.font.SysFont(font, font_size)
        if feedback == "":
            self.feedback = None
        else:
            self.feedback = feedback
        self.screen: pygame.surface.Surface = screen
        self.bg = bg
        self.color = color

        self.original_text: str = text
        self.text = self.font.render(self.original_text, True, self.color)
        self.text_pos = text_pos

        self.surface = None
        self.rect = None
        self.is_clicked = None

        self.image: pygame.surface.Surface = img
        self.image_pos = img_pos

        self.inner_bg = inner_bg

    def get_size_rect(self):
        if self.text_pos != (0, 0):
            return self.text.get_size()[0] + self.text_pos[0], self.text.get_size()[1] + self.text_pos[1]
        else:
            return self.text.get_size()[0], self.text.get_size()[1]

    def blit_button(self):
        # self.surface = pygame.Surface(self.get_size_rect()).convert_alpha()
        self.blit_background()
        self.rect = pygame.Rect(self.x, self.y, *self.get_size_rect())
        self.surface.blit(self.text, self.text_pos)

        self.is_clicked = False

    def blit_background(self):
        self.surface = pygame.Surface(self.get_size_rect()).convert_alpha()
        self.fill_background()
        if self.image is not None:
            self.surface.blit(self.image, self.image_pos)

    def fill_background(self):
        self.surface.fill(self.bg)

    def clicked(self):
        x, y = pygame.mouse.get_pos()
        clicked = None
        if self.rect.collidepoint(x, y):
            if pygame.mouse.get_pressed()[0]:
                pygame.time.wait(10)
                if not self.is_clicked:
                    if self.feedback is not None:
                        self.text = self.font.render(self.feedback, True, self.color)
                    self.is_clicked = True
                else:
                    self.text = self.font.render(self.original_text, True, self.color)
                    self.is_clicked = False
                self.blit_background()
                self.surface.blit(self.text, self.text_pos)
                self.rect = pygame.Rect(self.x, self.y, *self.get_size_rect())
                clicked = True
            else:
                self.surface.blit(self.text, (self.text_pos[0] + 1, self.text_pos[1] + 1))
                clicked = False
        else:
            self.blit_background()
            self.surface.blit(self.text, self.text_pos)
        return clicked

    def show(self):
        self.screen.blit(self.surface, (self.x, self.y))

    def reset(self):
        self.is_clicked = False
        self.text = self.font.render(self.original_text, True, self.color)
        self.blit_background()
        self.surface.blit(self.text, self.text_pos)
        self.rect = pygame.Rect(self.x, self.y, *self.get_size_rect())
