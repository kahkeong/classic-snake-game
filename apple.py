import random


class Apple:
    def __init__(self, map_length, appleColor):
        self.map_length = map_length
        self.color = appleColor
        self.x = map_length // 3
        self.y = map_length // 3

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
