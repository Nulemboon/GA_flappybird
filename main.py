import pygame
import random
from sys import exit
import config
import components
import population
import constants

pygame.init()
clock = pygame.time.Clock()
population = population.OtherPopulation(100)

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    pipes_spawn_time = 10
    font = pygame.font.Font(size=30)

    print("Generation 1")
    while True:
        quit_game()

        #draw background
        # config.window.fill((32, 32, 32)) 
        config.window.blit(constants.background_image, (0, 0))

        if len(config.ground) <= 2:
            config.ground.add(components.Ground(constants.window_width))

        #draw pipes
        if pipes_spawn_time <= 0:
            config.generate_pipes()
            pipes_spawn_time = random.randint(195, 230)
        pipes_spawn_time -= constants.scroll_speed

        config.pipes.draw(config.window)
        config.pipes.update()
        
        #draw ground
        config.ground.draw(config.window)   
        config.ground.update()

        #show score and generation
        score_text = font.render('Score: ' + str(constants.score), True, pygame.color.Color(32, 32, 32))
        config.window.blit(score_text, (20, 630))

        best_score_text = font.render('Best Score: ' + str(constants.best_score), True, pygame.color.Color(32, 32, 32))
        config.window.blit(best_score_text, (150, 630))

        gen_text = font.render('Generation: ' + str(population.generation), True, pygame.color.Color(32, 32, 32))
        config.window.blit(gen_text, (20, 660))

        #draw population
        if not population.extinct():
            population.update_live_players()
        else:
            constants.best_score = max(constants.score, constants.best_score)
            #print the last result
            print(f" Best score:{constants.best_score}")
            print(f" score: {constants.score}")
            constants.score = 0

            #restart with next generation
            config.pipes.empty()
            population.evolve()
            print(f"\nGeneration {population.generation}")

        clock.tick(300)
        pygame.display.flip()

main()