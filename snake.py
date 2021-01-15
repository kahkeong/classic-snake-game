from collections import deque


class Snake:
    def __init__(self, map_length, color, initial_direction):
        self.map_length = map_length
        self.direction = initial_direction
        self.body = deque()
        self.body.append((map_length // 2, map_length // 2))
        self.color = color

    def move(self):
        head_x, head_y = self.head()
        next_head_x, next_head_y = (
            head_x + self.direction[0],
            head_y + self.direction[1],
        )
        self.body.appendleft((next_head_x, next_head_y))
        self.body.pop()

    # notice here, we check the apple position with the next snake's head position
    # as if there is an apple, we dun pop from the snake body
    # eg  from      to   |  , by doing this, we do not need to remember the snake's tail direction
    #          |         |
    #         _|        _|
    # to achieve the same behaviour in a different way, we actually can move the entire snake first, then append an extra block to
    # the snake's tail to indicate the snake ate an apple, but this require us to remember the snake's tail direction
    def is_apple_eaten(self, apple):
        head_x, head_y = self.head()
        next_head_x, next_head_y = (
            head_x + self.direction[0],
            head_y + self.direction[1],
        )
        return (next_head_x, next_head_y) == apple.position()

    def update_direction(self, direction):
        self.direction = direction

    def is_snake_move_valid(self):
        head_x, head_y = self.head()
        next_head_x, next_head_y = (
            head_x + self.direction[0],
            head_y + self.direction[1],
        )

        # snake out of bound
        if not (
            0 <= next_head_x <= self.map_length - 1
            and 0 <= next_head_y <= self.map_length - 1
        ):
            return False

        # imagine next snake head will be at current snake end position, this is
        # valid since the head and end part move together simultaneously
        # eg head = 0, body = 1, end = 2 and snake move left
        # 2 0 1  in this case we return True,
        # 1   1  but this scenario will actually result to collision if head position is same as apple position at current round
        # 1 1 1  because we dun move end part when snake eat an apple, this result a delay of 1 move to lose
        if (next_head_x, next_head_y) == self.body[-1]:
            return True
        # snake head collides into its own body
        elif (next_head_x, next_head_y) in self.body:
            return False

        return True

    # the difference between grow and move is when growing, u dun pop the snake's tail
    def grow(self):
        head_x, head_y = self.head()
        next_head_x, next_head_y = (
            head_x + self.direction[0],
            head_y + self.direction[1],
        )
        self.body.appendleft((next_head_x, next_head_y))

    def head(self):
        return self.body[0]

    def length(self):
        return len(self.body)
