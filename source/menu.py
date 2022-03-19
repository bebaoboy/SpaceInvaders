from source.button import Button


class Menu:
    def __init__(self, font, font_size, screen, x_start, y_start,
                 space=50, bg=(0, 0, 0, 0), color='white'):
        self.screen = screen
        self.bg = bg
        self.x = x_start
        self.y = y_start
        self.space = space
        self.font = font
        self.font_size = font_size
        self.color = color

        self.menu_title = Button(
            self.font, self.font_size + 20, self.screen, "Space Invaders", (self.x, self.y - 200), self.bg)

        self.menu_dict = {
            'play': Button(
                self.font, self.font_size, self.screen, "Play", (self.x, self.y), self.bg),
            'quit': Button(
                self.font, self.font_size, self.screen, "Quit", (self.x, self.y + space), self.bg),
            'mute_sound': Button(
                self.font, self.font_size, self.screen, "Sound: on", (self.x, self.y + space * 3), self.bg,
                feedback='Sound: off'),
            'mute_music': Button(
                self.font, self.font_size, self.screen, "Music: on", (self.x, self.y + space * 4), self.bg,
                feedback='Music: off'),
            'crt': Button(
                self.font, self.font_size, self.screen, "Crt: on", (self.x, self.y + space * 5), self.bg,
                feedback='Crt: off')
        }
        for name, button in self.menu_dict.items():
            button.blit_button()

        self.menu_title.blit_button()

    def show(self):
        self.menu_title.show()

        for name, button in self.menu_dict.items():
            button.show()

    def reset(self):
        self.menu_dict['play'].reset()
