import components
import pygame
import constants
import random

window = pygame.display.set_mode((constants.window_width, constants.window_height))

ground = pygame.sprite.Group()
ground.add(components.Ground(0))

pipes = pygame.sprite.Group()

def generate_pipes():
    opening = random.randint(100, 130)
    x = constants.window_width
    y_top = random.randint(80, 350) - constants.pipe_top_image.get_height()
    y_bottom = y_top + constants.pipe_top_image.get_height() + opening
    pipes.add(components.Pipe(x, y_top, constants.pipe_top_image, 't'))
    pipes.add(components.Pipe(x, y_bottom, constants.pipe_bottom_image, 'b'))

button_speed_text = ["x1", "x2", "x5", "x10"]
speed = [60, 120, 300, 600]
speed_index = 0
button_rect = pygame.Rect(constants.window_width - 50, constants.window_height - 50, 40, 40)
