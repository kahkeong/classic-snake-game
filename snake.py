from collections import deque


class Snake:
    def __init__(self, map_length, color, initial_direction):
        self.map_length = map_length
        self.direction = initial_direction
        self.body = deque()
        self.body.append((map_length // 2, map_length // 2))
        self.color = color
        # in case we eat an apple, we add back this part
        self.last_popped_part = None

    def move(self):
        head_x, head_y = self.head()
        next_head_x, next_head_y = (
            head_x + self.direction[0],
            head_y + self.direction[1],
        )
        self.body.appendleft((next_head_x, next_head_y))
        self.last_popped_part = self.body.pop()

    def is_apple_eaten(self, apple):
        return self.head() == apple.position()

    def update_direction(self, direction):
        self.direction = direction

    def is_body_valid(self):
        head_x, head_y = self.head()

        # snake out of bound
        if not (
            0 <= head_x <= self.map_length - 1 and 0 <= head_y <= self.map_length - 1
        ):
            return False
        elif self.length() > 1:
            for part in self.body:
                # snake head collides into its own body
                if part != self.head() and part == self.head():
                    return False
        return True

    def grow(self):
        self.body.append(self.last_popped_part)

    def head(self):
        return self.body[0]

    def length(self):
        return len(self.body)
