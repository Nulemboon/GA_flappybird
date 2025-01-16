import pygame

#Assets
background_image = pygame.image.load("assets/background.png")
pipe_top_image = pygame.image.load("assets/pipe_top.png")
pipe_bottom_image = pygame.image.load("assets/pipe_bottom.png")
ground_image = pygame.image.load("assets/ground.png")

window_height = 720
window_width = 550
scroll_speed = 1
ground_level = 600
pipes_distance = 220
pipe_opening = 100
bird_start_pos = (100, 300)
score = 0
best_score = 0