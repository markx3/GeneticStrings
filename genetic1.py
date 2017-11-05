
import string
import random
from random import choice
import numpy as np
import os

lines = os.get_terminal_size().lines
chars = string.ascii_letters + ',' + '.' + ' '

class Individual:

    age = 0

    def __init__(self, lenght, dna=[], objective="", mutation=0.05):
        self.lenght = lenght
        self.fitness = 0
        self.objective = self.set_objective(objective)
        self.ilness = False
        if len(dna) == 0:
            self.dna = self.generate_dna()
        else:
            self.dna = dna
        self.mutation = mutation

    def crossover(self, other):
        new_dna = []
        half = random.randint(1, len(self.dna)-1)
        new_dna = self.dna[0:half] + other.dna[half:]
        res1 = Individual(self.lenght, dna=new_dna, objective=self.objective)
        res1.calc_fitness()
        res1.mutate()
        new_dna = other.dna[0:half] + self.dna[half:]
        res2 = Individual(self.lenght, dna=new_dna, objective=self.objective)
        res2.calc_fitness()
        res2.mutate()
        return res1, res2

    def mutate(self):
        #if self.fitness > random.uniform(0.0, 0.9):
        if self.mutation > random.uniform(0.0, 1.0):
            n = random.randint(0, (self.lenght // 2))
            for i in range(n):
                self.dna[random.randint(0, self.lenght-1)] = choice(chars)
            self.calc_fitness()

    def show(self):
        res = ""
        for letter in self.dna:
            res = res + letter
        print(res)

    def calc_fitness(self):
        fitness = 0.0
        for i in range(len(self.dna)):
            if self.dna[i] == self.objective[i]:
                fitness += 1.0
        self.fitness = fitness/len(self.dna)

    def set_objective(self, objective):
        res = []
        for char in objective:
            res.append(char)
        return res

    def generate_dna(self):
        res = []
        for char in self.objective:
            res.append(random.choice(chars))
        return res

class Population:

    gen = 1
    avg_fitness = 0
    found = False

    def __init__(self,
                 objective,
                 elitism=0.01,
                 num_ind=2048,
                 crossover=0.8,
                 mutation=0.05):
        self.objective  = objective
        self.num_individuals = num_ind
        self.elitism = elitism
        self.crossover = crossover
        self.mutation = mutation
        self.individuals = self.setup_population()

    def setup_population(self):
        l = len(self.objective)
        return [Individual(lenght=l,
                           objective=self.objective,
                           mutation=self.mutation)
                for n in range(self.num_individuals)]

    def tournament(self, individuals):
        best = choice(individuals)
        for i in range(3):
            adversary = choice(individuals)
            if (adversary.fitness > best.fitness):
                best = adversary
        return best

    def select_parents(self, individuals):
        p1 = self.tournament(individuals)
        p2 = self.tournament(individuals)
        if random.uniform(0, 1) < 0.8:
            return p1.crossover(p2)
        else:
            return p1, p2

    def trim_by_age(self, individuals):
        for ind in individuals:
            ind.age += 1
            if ind.age >= random.randint(80,100):
                individuals.remove(ind)

    def get_elite(self, best_individuals):
        idx = round(self.elitism * self.num_individuals)
        return best_individuals[:idx]

    def run(self):
        #self.trim_by_age(self.individuals)
        best_individuals = sorted(self.individuals,
                                  key = lambda x : x.fitness,
                                  reverse=True)
        self.avg_fitness = np.average([ind.fitness
                                       for ind in best_individuals])
        new_individuals = self.get_elite(best_individuals)

        while len(new_individuals) != self.num_individuals:
            c1, c2 = self.select_parents(best_individuals)
            new_individuals.append(c1)
            if len(new_individuals) == self.num_individuals: break
            new_individuals.append(c2)

        self.individuals = new_individuals
        self.gen += 1

        for ind in self.individuals:
            if ind.objective == ind.dna:
                self.found = True
                self.best_individual = ind

    def show(self):
        for ind in self.individuals:
            ind.show()
        print("Gen "
              + str(self.gen)
              + "\tavg. fitness: "
              + str(self.avg_fitness)
              + "\nElitism: " + str(self.elitism)
              + "\tPop. size: " + str(len(self.individuals)))


if __name__ == "__main__":
    obj = "Hello, world."
    #obj = "Unicorns are fun. Dinosaurs too. I like Llamas."
    obj = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis aliquet elit sed lorem suscipit ullamcorper. Mauris est felis, maximus eu congue nec, tincidunt imperdiet odio. Phasellus eu lacus vitae odio feugiat consectetur ut id neque. Morbi sed nisi vitae tortor facilisis tempus. Suspendisse pharetra eros in est ultrices imperdiet. Aliquam at sem ac nisl aliquet aliquet. Pellentesque nec ipsum id odio dignissim faucibus."
    population = Population(obj,
                            elitism=0.01,
                            num_ind=2048,
                            crossover=0.8,
                            mutation=0.05)
    while not population.found:
        population.run()
        population.show()
    population.best_individual.show()
