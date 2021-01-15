import pygame

from enum_game_state import GameState
from enum_map_size import MapSize
from enum_snake_direction import SnakeDirection
from snake import Snake
from apple import Apple


pygame.init()

BLOCK_SIZE = 20
INITIAL_SNAKE_DIRECTION = SnakeDirection.TOP
MAP_SIZE = MapSize.SMALL.value
WIDTH = BLOCK_SIZE * MAP_SIZE
HEIGHT = WIDTH
GAP = 2
FPS = 5

block_color = 0, 100, 255
apple_color = 255, 0, 0
snake_color = 0, 255, 100
main_menu_background_color = 0, 100, 255
gap_color = 0, 0, 0
text_color = 255, 153, 0

game_state = GameState.MAIN_MENU
snake = Snake(MAP_SIZE, snake_color, INITIAL_SNAKE_DIRECTION.value)
apple = Apple(MAP_SIZE, apple_color)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Comic Sans MS", 15)
big_font = pygame.font.SysFont("Comic Sans MS", 30)
clock = pygame.time.Clock()


# to create a thin line of gap between each block
# eg if block = # and line = $, default
#  ###  with this function  $$$
#  ###                      $#$
#  ###                      $$$
def rect_helper(coor_x, coor_y):
    return pygame.Rect(
        coor_x * BLOCK_SIZE + GAP,
        coor_y * BLOCK_SIZE + GAP,
        BLOCK_SIZE - 2 * GAP,
        BLOCK_SIZE - 2 * GAP,
    )


while True:
    clock.tick(FPS)

    # logic code start here
    if game_state == GameState.MAIN_MENU:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                game_state = GameState.IN_PROGRESS

    elif game_state == GameState.IN_PROGRESS:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_state = GameState.PAUSED

        if game_state != GameState.PAUSED:
            new_direction = snake.direction
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        new_direction = SnakeDirection.LEFT.value
                    elif event.key == pygame.K_RIGHT:
                        new_direction = SnakeDirection.RIGHT.value
                    elif event.key == pygame.K_UP:
                        new_direction = SnakeDirection.TOP.value
                    elif event.key == pygame.K_DOWN:
                        new_direction = SnakeDirection.BOTTOM.value

                # if length is 1, snake can move to any direction it like and
                # if new direction is same or is opposite, we skip (in each iteration of game loop,
                # multiple keys can be pressed at the same time)
                if snake.length() > 1 and (
                    snake.direction == new_direction
                    or (new_direction[0] * -1, new_direction[1] * -1) == snake.direction
                ):
                    pass
                else:
                    snake.update_direction(new_direction)
                    break

            snake.move()
            if snake.is_body_valid():
                if snake.is_apple_eaten(apple):
                    snake.grow()
                    apple.reposition(snake.body)
            else:
                game_state = GameState.END

    elif game_state == GameState.PAUSED:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_state = GameState.IN_PROGRESS

    else:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = GameState.IN_PROGRESS
                    snake = Snake(MAP_SIZE, snake_color, INITIAL_SNAKE_DIRECTION.value)
                    apple = Apple(MAP_SIZE, apple_color)

    # update screen code start here
    if game_state == GameState.MAIN_MENU:
        screen.fill(main_menu_background_color)
        start_surface = font.render("Press any key to start", True, text_color)
        start_rect = start_surface.get_rect(
            center=(MAP_SIZE // 2 * BLOCK_SIZE, MAP_SIZE // 2 * BLOCK_SIZE)
        )
        pause_game_tip_surface = font.render(
            "Press p to pause after game started", True, text_color
        )
        pause_game_tip_rect = pause_game_tip_surface.get_rect(
            center=(MAP_SIZE // 2 * BLOCK_SIZE, (MAP_SIZE // 2 + 1) * BLOCK_SIZE)
        )
        screen.blit(start_surface, start_rect)
        screen.blit(pause_game_tip_surface, pause_game_tip_rect)

    elif game_state == GameState.IN_PROGRESS:
        screen.fill(gap_color)
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                pygame.draw.rect(screen, block_color, rect_helper(x, y))

        for x, y in snake.body:
            pygame.draw.rect(screen, snake.color, rect_helper(x, y))

        score_surface = font.render(f"Score: {snake.length()}", True, text_color)
        screen.blit(score_surface, (0, 0))
        pygame.draw.rect(screen, apple.color, rect_helper(apple.x, apple.y))

    elif game_state == GameState.PAUSED:
        pause_surface = big_font.render("Game paused", True, text_color)
        pause_rect = pause_surface.get_rect(
            center=(
                MAP_SIZE // 2 * BLOCK_SIZE,
                MAP_SIZE // 2 * BLOCK_SIZE,
            )
        )
        screen.blit(pause_surface, pause_rect)
    else:
        score_surface = font.render(
            f"You lose, Score: {snake.length()}", True, text_color
        )
        score_rect = score_surface.get_rect(
            center=(MAP_SIZE // 2 * BLOCK_SIZE, MAP_SIZE // 2 * BLOCK_SIZE)
        )

        play_again_surface = font.render("Press space to restart", True, text_color)
        play_again_rect = score_surface.get_rect(
            center=(MAP_SIZE // 2 * BLOCK_SIZE, (MAP_SIZE // 2 + 1) * BLOCK_SIZE)
        )

        screen.fill(main_menu_background_color)
        screen.blit(score_surface, score_rect)
        screen.blit(play_again_surface, play_again_rect)

    pygame.display.flip()
