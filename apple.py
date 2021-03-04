import random
import pygame
from helper import rect_helper


class Apple:
    def __init__(self, map_length, apple_color):
        self.map_length = map_length
        self.color = apple_color
        self.x = random.randint(0, map_length - 1)
        self.y = random.randint(0, map_length - 1)

    def position(self):
        return (self.x, self.y)

    def reposition(self, snake_body):
        possible_positions = set()
        for x in range(self.map_length):
            for y in range(self.map_length):
                possible_positions.add((x, y))

        for x, y in snake_body:
            possible_positions.remove((x, y))

        next_position = random.sample(possible_positions, 1)[0]
        self.x = next_position[0]
        self.y = next_position[1]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, rect_helper(self.x, self.y))
