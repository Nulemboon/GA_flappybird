import random
import pygame
import config
import model

class Player(pygame.sprite.Sprite):
    birds = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #for bird
        self.x, self.y = 50, 300
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.velocity = 0
        self.flap = False
        self.living = True
        self.lifespan = 0

        #for model
        self.decision = None
        self.position = [0.5, 0.5]
        self.inputs = 2
        self.model = model.Model(self.inputs)
        self.model.generate()
        self.fitness = 0

        Player.birds += 1

    #Functions in game
    def draw(self, window):
        pygame.draw.rect(window, (0, 180, 220), self.rect, 
                         width = 0,
                         border_top_left_radius=16,
                         border_bottom_left_radius=14,
                         border_top_right_radius=10,
                         border_bottom_right_radius=10)
        pygame.draw.rect(window, (32, 32, 32), self.rect, 
                         width = 1,
                         border_top_left_radius=18,
                         border_bottom_left_radius=12,
                         border_top_right_radius=15,
                         border_bottom_right_radius=15)
        eye = pygame.Rect(self.rect.right - 12, self.rect.top - 1, 10, 10)
        beak = pygame.Rect(self.rect.right - 10, self.rect.top + 10, 12, 8)
        wing = pygame.Rect(self.rect.left - 2, self.rect.top + 10, 10, 6)

        pygame.draw.rect(window, (240, 240, 240), eye,
                         border_top_left_radius=5,
                         border_bottom_left_radius=5,
                         border_top_right_radius=5,
                         border_bottom_right_radius=5)
        pygame.draw.rect(window, (32, 32, 32), eye,
                         width=1,
                         border_top_left_radius=5,
                         border_bottom_left_radius=5,
                         border_top_right_radius=5,
                         border_bottom_right_radius=5)
        pygame.draw.rect(window, (32, 32, 32), pygame.Rect(eye.centerx + 1, eye.centery, 2, 2), width=2)
        
        pygame.draw.rect(window, (120, 90, 90), beak,
                         border_top_left_radius=4,
                         border_bottom_left_radius=3,
                         border_top_right_radius=2,
                         border_bottom_right_radius=6)
        pygame.draw.rect(window, (32, 32, 32), beak,
                         width=1,
                         border_top_left_radius=4,
                         border_bottom_left_radius=2,
                         border_top_right_radius=2,
                         border_bottom_right_radius=4)
        
        pygame.draw.rect(window, (240, 240, 240), wing,
                         border_top_left_radius=2,
                         border_bottom_left_radius=6,
                         border_top_right_radius=3,
                         border_bottom_right_radius=3)
        pygame.draw.rect(window, (32, 32, 32), wing,
                         width=1,
                         border_top_left_radius=2,
                         border_bottom_left_radius=6,
                         border_top_right_radius=3,
                         border_bottom_right_radius=3)

    def ground_collision(self, ground):
        for g in ground:
            if pygame.Rect.colliderect(self.rect, g):
                return True
        return False        
    
    def sky_collision(self):
        return bool(self.rect.y < 50)
    
    def pipe_collision(self):
        for p in config.pipes:
            if pygame.Rect.colliderect(self.rect, p.rect):
                return True
        return False
        
    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            #gravity 
            self.velocity += 0.25
            self.rect.y += self.velocity
            if self.velocity > 5:
                self.velocity = 5
            #increase lifespan
            self.lifespan += 1
        else:
            #bird died
            Player.birds -= 1
            self.living = False
            self.flap = False
            self.velocity = 0

    def bird_flap(self):
        #avoid continuous flapping and flapping over the top
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.velocity = -5
        if self.velocity >= 0:
            self.flap = False

    @staticmethod
    def next_pipe():
        for i in range(0, len(config.pipes.sprites())):
            if not config.pipes.sprites()[i].passed:
                return config.pipes.sprites()[i], config.pipes.sprites()[i + 1]
    #Function for training AI
    def look(self):
        if config.pipes:
            top_rect, bottom_rect = self.next_pipe()
            #height difference
            self.position[0] = max(0, self.rect.center[1] - (top_rect.rect.bottom + bottom_rect.rect.top) / 2) / 600
            pygame.draw.line(config.window, self.color, self.rect.center,
                              (self.rect.center[0], (top_rect.rect.bottom + bottom_rect.rect.top) / 2))
            
            #horizontal distance
            self.position[1] = max(0, top_rect.rect.x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                                (top_rect.rect.x, self.rect.center[1]))

    def think(self):
        self.decision = self.model.feed_forward(self.position)
        if Player.birds == 1:
            for i in range(len(self.model.edges)):
                print(self.model.edges[i].weight)
        if self.decision > 0.6:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.model = self.model.clone()
        clone.model.generate()

        return clone
