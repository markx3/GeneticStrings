
import string
import random
from random import choice
#from numpy.random import choice
import numpy as np
from numpy import cumsum
from numpy.random import rand
import os
from numba import jit

lines = os.get_terminal_size().lines
chars = string.ascii_letters + ',' + '.' + ' '

class Individual:
    def __init__(self, lenght, dna=[], objective=""):
        self.lenght = lenght
        self.fitness = 0
        self.objective = self.set_objective(objective)
        self.ilness = False
        if len(dna) == 0:
            self.dna = self.generate_dna()
        else:
            self.dna = dna

    def crossover(self, other):
        new_dna = []
        # for i in range(len(self.dna)):
        #     if i % 2 == 0:
        #         new_dna.append(self.dna[i])
        #     else:
        #         new_dna.append(other.dna[i])

        half = len(self.dna) // 2
        new_dna = self.dna[0:half] + other.dna[half:]
        res = Individual(self.lenght, dna=new_dna, objective=self.objective)
        res.calc_fitness()
        res.mutate()
        return res

    def mutate(self):
        #if self.fitness > random.uniform(0.0, 0.9):
        if random.uniform(0.0, 0.5) <= random.uniform(0.0, 1.0):
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



#obj = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse molestie ut nisi et condimentum. Proin pharetra, neque ut eleifend dignissim, sapien est aliquet lorem, at ullamcorper quam libero eget orci. Nunc dapibus dui quis nisi sodales, ac pharetra neque porttitor. Pellentesque rutrum vestibulum volutpat. Quisque tincidunt auctor dolor, eu ultricies mi suscipit quis. Nam dolor metus, facilisis nec lorem aliquam, lacinia sollicitudin neque. Morbi at egestas eros."
obj = "Unicorns are fun. Dinosaurs too."
#obj = "hello, worldee"
num_individuals = 2048
modifier = 0.01 # Selection easening
gen = 1
elitism = 0.1

def tournament(population):
    best = choice(population)
    for i in range(3):
        aux = choice(population)
        if (aux.fitness > best.fitness): best = aux
    return best

pop = [Individual(lenght=len(obj), objective=obj) for n in range(num_individuals)]
print(pop[1].dna)
print(pop[1].objective)
current_fitness = 0
found = False
for ind in pop:
    ind.calc_fitness()

idx = round(elitism * num_individuals)

while 1:


    #pop_best = list(filter(lambda x : x.fitness > current_fitness-modifier, pop))
    best_individuals = sorted(pop, key = lambda x : x.fitness, reverse=True)
    fitness_list = [ind.fitness for ind in best_individuals]
    current_fitness = np.average(fitness_list)

    print("Gen " + str(gen) + "\tavg. fitness: " + str(current_fitness)
         + "\tElitism: " + str(elitism))
    print()

    new_gen = []

    while len(new_gen) != num_individuals:
        ind1 = tournament(best_individuals[:idx])
        ind2 = tournament(best_individuals[:idx])
        if random.uniform(0, 1) <= 0.8:
            new_gen.append(ind1.crossover(ind2))
            new_gen.append(ind2.crossover(ind1))

    pop = new_gen
    gen += 1
    for ind in pop:
        #ind.show()
        if ind.dna == ind.objective:
            ind.show()
            print(gen)
            found = True
            break
    if found:
        print("Population avg fitness:" + str(current_fitness))
        break

    elitism = (current_fitness / 10) * 2
