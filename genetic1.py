
import string
import random
from numpy.random import choice
import numpy as np
from numpy import cumsum
from numpy.random import rand
def weightedChoice(weights, objects):
    """Return a random item from objects, with the weighting defined by weights
    (which must sum to 1)."""
    cs = cumsum(weights) #An array of the weights, cumulatively summed.
    idx = sum(cs < rand()) #Find the index of the first weight over a random value.
    return objects[idx]

chars = string.ascii_letters + ',' + '.' + ' '

class Individual():
    def __init__(self, lenght, dna=[], objective=""):
        self.lenght = lenght
        self.fitness = 0
        self.objective = self.set_objective(objective)
        if len(dna) == 0:
            self.dna = self.generate_dna()
        else:
            self.dna = dna

    def crossover(self, other):
        half = len(self.dna) // 2
        new_dna = self.dna[0:half] + other.dna[half:]
        res = Individual(self.lenght, dna=new_dna, objective=self.objective)
        res.mutate()
        return res

    def mutate(self):
        if self.fitness < random.uniform(0.2, 1.0):
            n = random.randint(0, (self.lenght // 2)-1)
            for i in range(n):
                self.dna[random.randint(0, self.lenght-1)] = random.choice(chars)

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



obj = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse molestie ut nisi et condimentum. Proin pharetra, neque ut eleifend dignissim, sapien est aliquet lorem, at ullamcorper quam libero eget orci. Nunc dapibus dui quis nisi sodales, ac pharetra neque porttitor. Pellentesque rutrum vestibulum volutpat. Quisque tincidunt auctor dolor, eu ultricies mi suscipit quis. Nam dolor metus, facilisis nec lorem aliquam, lacinia sollicitudin neque. Morbi at egestas eros. Nunc molestie, turpis id iaculis congue, diam elit commodo tellus, a eleifend risus nibh eu lacus. Nunc pellentesque dui et quam aliquet, eget auctor ipsum porttitor."
obj = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
num_individuals = 100
modifier = 0 # Selection easening

pop = [Individual(lenght=len(obj), objective=obj) for n in range(num_individuals)]
print(pop[1].dna)
print(pop[1].objective)
current_fitness = 0
found = False
while 1:
    for ind in pop:
        ind.show()
        ind.calc_fitness()
        if ind.dna == ind.objective:
            ind.show()
            found = True
            break
    if found:
        print("Population avg fitness:" + str(current_fitness))
        break


    pop_best = list(filter(lambda x : x.fitness > np.random.uniform(current_fitness-modifier, current_fitness), pop))
    best_individuals = sorted(pop_best, key = lambda x : x.fitness, reverse=True)
    fitness_list = [ind.fitness for ind in best_individuals]
    new_fitness = np.average(fitness_list)
    if current_fitness < new_fitness:
        current_fitness = new_fitness
    #print(fitness_list)
    print(current_fitness)
    print(len(pop_best))
    if len(pop_best) < 10:
        modifier += 0.1
        print("Mod up!")
    if modifier >= 0.5 and len(pop_best) >= 10:
        modifier -= 0.1
        print("Mod too high, going down.")


    new_gen = []
    for _ in range(num_individuals):
        ind1 = weightedChoice(fitness_list, best_individuals)
        ind2 = weightedChoice(fitness_list, best_individuals)
        new_gen.append(ind1.crossover(ind2))

    pop = new_gen
