import pygame


def display_ingame_text(screen, font, text, x, y, x_scale=1.0, y_scale=1.0, color='white'):
    surf = font.render(text.upper(), False, color)
    surf = pygame.transform.scale(
        surf, (surf.get_width() * x_scale, surf.get_height() * y_scale))
    rect = surf.get_rect(
        center=(x, y))
    screen.blit(surf, rect)
