import pygame
import constants

class Ground(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = constants.ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, constants.ground_level
    
    def update(self):
        self.rect.x -= constants.scroll_speed
        if self.rect.x <= -constants.window_width:
            self.kill()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.type = pipe_type
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.passed = False
        self.off_screen = False

    def update(self):
        self.rect.x -= constants.scroll_speed
        if self.passed == False and self.rect.x + self.rect.width <= 50:
            self.passed = True
            if self.type == 'b': constants.score += 1
        if self.rect.x + self.rect.width <= 0:
            self.off_screen = True
            self.kill()