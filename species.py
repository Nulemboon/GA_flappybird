import operator
import random

# THRESHOLD = 1.2

class Species:
    def __init__(self, player):
        self.players = []
        self.avg_fitness = 0
        self.threshold = 1.2
        self.players.append(player)
        self.fitness_score = player.fitness
        self.meta_model = player.model.clone()
        self.best = player.clone()
        self.stale = 0

    def is_similar(self, model):
        diff = 0
        for i in range(0, len(self.meta_model.edges)):
            diff += abs(self.meta_model.edges[i].weight - model.edges[i].weight)
        
        return diff < self.threshold
    
    def is_stale(self):
        return self.stale >= 8

    def add_player(self, player):
        self.players.append(player)

    def calculate_fitness(self):
        #calculate mean fitness
        self.avg_fitness = 0
        for p in self.players:
            self.avg_fitness += p.fitness
        
        if len(self.players) > 0:
            self.avg_fitness = int(self.avg_fitness / len(self.players))

    def sort_by_fitness(self):
        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)
        if self.players[0].fitness > self.fitness_score:
            self.fitness_score = self.players[0].fitness
            self.best = self.players[0].clone()
            self.stale = 0
        else: self.stale += 1

    def offspring(self):
        child = self.players[random.randint(1, len(self.players)) - 1].clone()
        child.model.mutate()
        return child
