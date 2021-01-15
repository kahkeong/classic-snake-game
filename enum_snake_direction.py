from enum import Enum


class SnakeDirection(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    TOP = (0, -1)
    BOTTOM = (0, 1)
