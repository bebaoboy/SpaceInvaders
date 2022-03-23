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

        self.leaderboard = []
        self.high_scores = []
        self.leaderboard.append(
            Button(
                self.font, self.font_size - 3, self.screen, f"Leaderboard",
                (self.x + 480, self.y + space / 3), self.bg)
        )
        self.max_highscore = 5

    def show(self):
        self.menu_title.show()

        for name, button in self.menu_dict.items():
            button.show()

        for score in self.leaderboard:
            score.show()

    def add_highscore(self, high_scores):
        while len(self.leaderboard) != 1:
            self.leaderboard.pop()
        self.high_scores.extend(_ for _ in high_scores if _ not in self.high_scores)
        self.high_scores = sorted(self.high_scores, reverse=True)
        if len(self.high_scores) < self.max_highscore:
            self.max_highscore = len(self.high_scores)

        for i, score in enumerate(self.high_scores[:self.max_highscore]):
            self.leaderboard.append(
                Button(
                    self.font, self.font_size - 4, self.screen, f"{i + 1}. {score:>8}",
                    (self.x + 485, self.y + self.space / 2 * i + self.space), self.bg)
            )
        print(self.high_scores)
        for score in self.leaderboard:
            score.blit_button()
        return self.high_scores

    def reset(self):
        self.menu_dict['play'].reset()
