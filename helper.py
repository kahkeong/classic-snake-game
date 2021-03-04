import pygame
import config as c

# to create a thin line of gap between each block
# eg if block = # and line = $, default
#  ###  with this function  $$$
#  ###                      $#$
#  ###                      $$$
def rect_helper(coor_x, coor_y):
    return pygame.Rect(
        coor_x * c.BLOCK_SIZE + c.GAP,
        coor_y * c.BLOCK_SIZE + c.GAP,
        c.BLOCK_SIZE - 2 * c.GAP,
        c.BLOCK_SIZE - 2 * c.GAP,
    )