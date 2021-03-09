from collections import defaultdict
import pygame
import sys
import config as c
from text import Text
from enum_game_state import GameState
from enum_snake_direction import SnakeDirection
from snake import Snake
from apple import Apple
from helper import rect_helper


class Game:
    def __init__(self):
        self.state = GameState.MAIN_MENU
        self.snake = None
        self.apple = None
        self.surface = None
        self.objects = defaultdict(list)
        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.font = pygame.font.SysFont("Comic Sans MS", 15)
        self.surface = pygame.display.set_mode((c.WIDTH, c.HEIGHT))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.IN_PROGRESS:
                    new_direction = self.snake.direction

                    if event.key == pygame.K_LEFT:
                        new_direction = SnakeDirection.LEFT.value
                    elif event.key == pygame.K_RIGHT:
                        new_direction = SnakeDirection.RIGHT.value
                    elif event.key == pygame.K_UP:
                        new_direction = SnakeDirection.TOP.value
                    elif event.key == pygame.K_DOWN:
                        new_direction = SnakeDirection.BOTTOM.value
                    elif event.key == pygame.K_p:
                        self.state = GameState.PAUSED

                    # if length is 1, snake can move to any direction it like and
                    # if new direction is same or is opposite, we skip (in each iteration of game loop,
                    # multiple keys can be pressed at the same time)
                    if len(self.snake) > 1 and (
                        self.snake.direction == new_direction
                        or (new_direction[0] * -1, new_direction[1] * -1)
                        == self.snake.direction
                    ):
                        pass
                    else:
                        self.snake.update_direction(new_direction)
                        break

                elif self.state == GameState.MAIN_MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.IN_PROGRESS

                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        self.state = GameState.IN_PROGRESS

                elif self.state == GameState.END:
                    if event.key == pygame.K_SPACE:
                        self.setup()
                        self.state = GameState.IN_PROGRESS

    def draw_grid(self):
        for x in range(c.MAP_SIZE):
            for y in range(c.MAP_SIZE):
                pygame.draw.rect(self.surface, c.BLOCK_COLOR, rect_helper(x, y))

    def draw(self):
        self.draw_grid()
        self.snake.draw(self.surface)
        self.apple.draw(self.surface)

        for obj in self.objects[self.state]:
            obj.draw(self.surface)

    def update(self):
        if self.state == GameState.IN_PROGRESS:
            self.snake.update()

            if self.snake.is_body_valid():
                if self.snake.can_eat_apple(self.apple):
                    self.snake.grow()
                    self.apple.reposition(self.snake.body)
            else:
                self.state = GameState.END

    def setup(self):
        self.snake = Snake(c.MAP_SIZE, c.SNAKE_COLOR)
        self.apple = Apple(c.MAP_SIZE, c.APPLE_COLOR)
        pause_hint_text = Text(
            0,
            0,
            lambda: "Press p to pause/unpause after game started",
            self.font,
            True,
        )
        start_text = Text(0, 50, lambda: "Press space to start", self.font, True)
        score_text = Text(0, 0, lambda: f"Score: {len(self.snake)}", self.font)
        play_again_text = Text(
            0,
            0,
            lambda: f"You lose! Final Score: {len(self.snake)}. Press space to restart",
            self.font,
            True,
        )
        pause_text = Text(0, 0, lambda: "Game paused", self.font, True)

        self.objects[GameState.MAIN_MENU] = [pause_hint_text, start_text]
        self.objects[GameState.PAUSED] = [pause_text]
        self.objects[GameState.IN_PROGRESS] = [score_text]
        self.objects[GameState.END] = [play_again_text]

    def run(self):
        pygame.display.set_caption("Snake game")
        self.setup()

        while True:
            self.surface.fill(c.BACKGROUND_COLOUR)
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(c.FPS)


def main():
    Game().run()


if __name__ == "__main__":
    main()