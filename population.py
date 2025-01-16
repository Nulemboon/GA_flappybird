import config
import player
import math
import random
import species
import operator

class Population:
    def __init__(self, population_size):
        self.players = []
        self.generation = 1
        self.size = population_size
        for i in range(0, self.size):
            self.players.append(player.Player())


    def update_live_players(self):
        for p in self.players:
            if p.living:
                p.look()
                p.think()
                p.draw(config.window)
                p.update(config.ground)

    def selection(self):
        #calculate players' fitness
        for p in self.players:
            p.calculate_fitness()

        #sort by players' fitness
        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)

    @staticmethod
    def crossover(player_a, player_b):
        cutoff = random.randint(0, len(player_a.model.neurons) - 1)

        for i in range(cutoff, len(player_a.model.neurons)):
            temp = player_a.model.neurons[i].bias
            player_a.model.neurons[i].bias = player_b.model.neurons[i].bias
            player_b.model.neurons[i].bias = temp

        return random.choice((player_a, player_b))

    def next_gen(self):
        nextgen = []

        #take the best quarter of the previous generation
        for i in range(0, self.size // 4):
            nextgen.append(self.players[i].clone())

        #crossover the next quarter
        for i in range(0, self.size // 4):
            first = random.randint(0, self.size // 4 - 1)
            second = random.randint(0, self.size // 4 - 1)
            nextgen.append(self.crossover(nextgen[first].clone(), nextgen[second].clone()))
        
        #mutate the left half
        while len(nextgen) < self.size:
            offspring = self.players[random.randint(0, self.size - 1)].clone()
            offspring.model.mutate()
            nextgen.append(offspring)
        
        self.players = []
        for n in nextgen:
            self.players.append(n)
        self.generation += 1

    def evolve(self):
        #selection
        self.selection()

        #next generation
        self.next_gen()

    def extinct(self):
        for p in self.players:
            if p.living:
                return False
        return True
    

class OtherPopulation(Population):
    def __init__(self, pop_size):
        Population.__init__(self, pop_size)
        self.species = []

    def speciate(self):
        #clear the old species instances
        for s in self.species:
            s.players = []
        
        for p in self.players:
            flag = False
            #add to existing species if the model is similar
            for s in self.species:
                if s.is_similar(p.model):
                    s.add_player(p)
                    flag = True
                    break
            #else create new species
            if not flag:
                self.species.append(species.Species(p))

    def delete_extinct_species(self):
        extinct_species = [s for s in self.species if len(s.players) == 0]
        for s in extinct_species:
            self.species.remove(s)
    
    def delete_stale_species(self):
        stale_players = []
        stale_species = []

        for s in self.species:
            if s.is_stale():
                if len(stale_species) + 1 < len(self.species):
                    stale_species.append(s)
                    for p in s.players:
                        stale_players.append(p)
                else: s.stale = 0

        for p in stale_players:
            self.players.remove(p)
        for s in stale_species:
            self.species.remove(s)

    def selection(self):
        super().selection()

        #get mean fitness value of all instances in the species
        for s in self.species:
            s.calculate_fitness()
        
        #delete extinct and stale species
        self.delete_extinct_species()
        self.delete_stale_species()

        #sort species by fitness
        for s in self.species:
            s.sort_by_fitness()
        
        self.species.sort(key=operator.attrgetter('fitness_score'), reverse=True)
    
    def next_gen(self):
        nextgen = []

        #add the best of each species to the next gen
        for s in self.species:
            nextgen.append(s.best.clone())
        
        #Fill the slots by the children of each species equally
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))
        for s in self.species:
            for i in range(0, children_per_species):
                nextgen.append(s.offspring())

        #Fill the left slots by children of the best species
        while len(nextgen) < self.size:
            nextgen.append(self.species[0].offspring())

        self.players = []
        for i in nextgen:
            self.players.append(i)
        self.generation += 1

    def evolve(self):
        #create species
        self.speciate()

        super().evolve()

