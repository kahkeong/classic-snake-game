import config as c
import pygame


class Text:
    def __init__(
        self,
        x,
        y,
        text_func,
        font,
        centre_x=False,
        color=c.TEXT_COLOR,
    ):
        self.centre_x = centre_x
        self.pos = x, y
        self.text_func = text_func
        self.color = color
        self.font = font

    def draw(self, surface):
        if self.centre_x:
            center = surface.get_rect().center
            text_surface = self.font.render(self.text_func(), True, self.color)
            pos = text_surface.get_rect(center=center)
            # relative to middle of screen
            pos.x += self.pos[0]
            pos.y += self.pos[1]
            surface.blit(text_surface, pos)
        else:
            text_surface = self.font.render(self.text_func(), True, self.color)
            surface.blit(text_surface, self.pos)

    def rect(self):
        text_surface = self.font.render(self.text_func(), True, self.color)
        return text_surface.get_rect()
