import random
import logging
import matplotlib.pyplot as plt

log = logging.getLogger()


class GeneticAlgorithm:
    class Group:
        """ Contain a group of indexes. """
        def __init__(self, indexes: list) -> None:
            self.indexes = indexes

    def __init__(self, fitness_function_cb, chromosome_size: int, population_size: int = 100,
                 mutation_rate: float = 0.1, nr_of_levels: int = 1, group_size: int = 2, binary: bool = False) -> None:
        self.fitness_function_cb = fitness_function_cb
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.binary = binary
        self.groups = self._get_groups(chromosome_size, nr_of_levels, group_size)
        self.population = self._get_initial_population(population_size, self.groups)

    def plot_history(self, history: list) -> None:
        """ Plot the training history. """
        plt.plot([x for x in range(len(history))], history)
        plt.show()

    def run(self, generations_per_level: int) -> list:
        """ Returns best solution. """
        history = []
        for level in range(len(self.groups)-1, 0, -1):
            self._sort_population(level)
            for generation in range(generations_per_level):
                self._breed()
                self._sort_population(level)
                self.population = self.population[:self.population_size]
                history.append(self._get_fitness(self.population[0], level))
            self._uncoarsen_population(level, level-1)
        print('best fitness:', self.fitness_function_cb(self.population[0]))
        print('best solution:', self.population[0])
        self.plot_history(history)
        return self.population[0]

    @staticmethod
    def _get_groups(chromosome_size: int, nr_of_levels: int, group_size: int) -> list:
        """ Creates group definitions used for level transitions. """
        res = [[i for i in range(chromosome_size)]]
        previous_layer_size = len(res[0])
        for _ in range(nr_of_levels):
            if previous_layer_size == 1:
                log.warning('too many levels')
                break
            groups_current_level = []
            available_indexes = [i for i in range(previous_layer_size)]
            random.shuffle(available_indexes)
            while len(available_indexes) > 0:
                if len(available_indexes) <= group_size:
                    groups_current_level.append(GeneticAlgorithm.Group(available_indexes))
                    break
                else:
                    groups_current_level.append(GeneticAlgorithm.Group(available_indexes[:group_size]))
                    available_indexes = available_indexes[group_size:]
            previous_layer_size = len(groups_current_level)
            res.append(groups_current_level)
        return res

    def _get_random(self):
        """ Returns a random value. """
        return random.randint(0, 1) if self.binary else random.uniform(0., 1.)

    def _get_initial_population(self, population_size: int, groups: list) -> list:
        """ Creates the initial population. """
        res = []
        for _ in range(population_size):
            chromosome = []
            for _ in range(len(groups[-1])):
                chromosome.append(self._get_random())
            res.append(chromosome)
        return res

    @staticmethod
    def _two_point_crossover(parent_a: list, parent_b: list) -> (list, list):
        """ Breeds to selected parents and returns two children. """
        indexes = [random.randint(0, len(parent_a)-1), random.randint(0, len(parent_a)-1)]
        indexes.sort()
        child_a, child_b = [], []
        for i in range(len(parent_a)):
            if indexes[0] <= i <= indexes[1]:
                child_a.append(parent_b[i])
                child_b.append(parent_a[i])
            else:
                child_a.append(parent_a[i])
                child_b.append(parent_a[i])
        return child_a, child_b

    def _mutate(self, chromosome) -> list:
        """ Mutates a single chromosome. """
        for i in range(len(chromosome)):
            if random.random() <= self.mutation_rate:
                chromosome[i] = self._get_random()
        return chromosome

    def _breed(self):
        """ Breeds the population. """
        for i in range(0, len(self.population), 2):
            child_a, child_b = self._two_point_crossover(self.population[i], self.population[i+1])
            self.population.append(self._mutate(child_a))
            self.population.append(self._mutate(child_b))

    def _get_fitness(self, chromosome: list, level: int):
        """ Measure the fitness of a single chromosome. """
        return self.fitness_function_cb(self._uncoarsen(chromosome, level, 0))

    def _sort_population(self, current_level: int) -> None:
        """ Sort population best to worst. """
        self.population = sorted(self.population, key=lambda x: self._get_fitness(x, current_level))

    def _uncoarsen(self, chromosome: list, from_level: int, to_level: int) -> list:
        """ Uncoarsens a single chromosome to a specified level. """
        if from_level == 0 or from_level == to_level:
            return chromosome
        res = chromosome
        for current_level in range(from_level, to_level, -1):
            un_coarsened_chromosome = [0 for _ in range(len(self.groups[current_level-1]))]
            j = 0
            for group in self.groups[current_level]:
                for i in group.indexes:
                    un_coarsened_chromosome[i] = res[j]
                j += 1
            res = un_coarsened_chromosome
        return res

    def _uncoarsen_population(self, from_level: int, to_level: int):
        """ Uncoarsens the entire population to a specified level. """
        for i in range(len(self.population)):
            self.population[i] = self._uncoarsen(self.population[i], from_level, to_level)


def fitness_function(chromosome: list) -> float:
    return sum(chromosome)


def main():
    ga = GeneticAlgorithm(fitness_function, chromosome_size=10, population_size=100, nr_of_levels=2, group_size=2,
                          binary=False)
    ga.run(100)


if __name__ == '__main__':
    main()
