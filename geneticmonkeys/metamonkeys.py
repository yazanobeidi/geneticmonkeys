"""
This is a companion script to geneticmonkeys.py

The purpose of this script is to automatically and repeatedly run geneticmonkeys
to find optimal parameters, and to generate useful insights based on performance
statistics.

Rather than a purely straightforward statistical approach, i.e. testing a range
of parameters for the best one, which of course would work but is rather dull,
we use a genetic algorithm, hence the name metamonkeys.

TODO: better reporting in display_results().
"""

import numpy as np
import string
import argparse
import sys
import bisect
import time
from math import floor

from geneticmonkeys import Environment, Monkey
import evolution
import gmutils

__author__ = 'Yazan Obeidi'
__copyright__ = 'Copyright 2016, Yazan Obeidi'
__license__ = 'GPLv3'
__version__ = '0.0.2'
__maintainer__ = 'Yazan'
__status__ = 'development'

# TODO: Eventually move to config.cfg:
# Meta Genetic Variables
META_MAX_POP = 100
META_MUTATION_RATE = 0.3
META_MUTATION_SIGNIFICANCE = 0.01
META_BIRTH_RATE = 1
META_MORTALITY_RATE = 0
# Seed Variables
PHRASE = 'To be'
# Genetic Seed Variables
MORTALITY_RATE = 0
MUTATION_RATE = 0.17
BIRTH_RATE = 1
MAX_POP = 100
# Symbols
STRING_SET = string.letters + string.punctuation + ' '

class Universe(object):
    """
    Abstraction that contains multiple Environments (max_pop to be precise).
    """
    def __init__(self, **kwargs):
        seed = kwargs['seed']
        self.phrase = kwargs['phrase']
        self.max_pop = int(kwargs['max_pop'])
        self.mortality_rate = float(kwargs['mortality_rate'])
        self.birth_rate = float(kwargs['birth_rate'])
        self.mutation_rate = float(kwargs['mutation_rate'])
        self.mutation_significance = float(kwargs['mutation_significance'])
        self.size = len(self.phrase)
        self.avg_score = float()
        self.metamonkeys = gmutils.GMList()
        self.cumdist = list()
        self.num_complete = int()
        self.invcumdist = list()
        self.results = list()
        self.generations = int()
        self.best_dnas = list()
        self.now = time.clock()
        print 'Spawning metamonkeys!'
        for i in xrange(0, self.max_pop):
            self.metamonkeys.append(MetaMonkey(self.phrase, **seed))
        print ''

    def evolve(self):
        """
        Once a monkey via metamonkey has found the solution we do not touch it.
        It's DNA becomes available for reproduction, until replaced through
        selection / reproduction.
        """
        all_complete = False
        self.now = time.clock()
        while not all_complete:
            #print '\n'
            print 'gen. {} : running: {} num_complete: {} avg_score: {}       '\
                  '                                           \r'\
                  .format(self.generations, len(self.metamonkeys), 
                  self.num_complete, str.format('{0:.4f}', self.avg_score)),
            self.select()
            print ''
            for metamonkey in self.metamonkeys:
                if metamonkey.found:
                    if all_complete: all_complete = True
                    self.num_complete += 1
                    result_text = 'SUCCESS ({t}s)! {n} gen: {g} subgen: {sg} '\
                                  'phrase : {p} time : {st} : fitness : {f} '\
                                  'dna: {d}'.format(n=metamonkey, 
                                  t=time.clock() - self.now, d=metamonkey.dna,
                                  st=metamonkey.elapsed_time,
                                  g=self.generations, sg=metamonkey.generation,
                                  p=metamonkey.string, f=metamonkey.fitness)
                    print result_text
                    self.results.append(result_text)
                    self.best_dnas.append(metamonkey.dna)
                    continue
                else:
                    all_complete = metamonkey.evolve()
            self.generations += 1
            #print ''
            self.reproduce()
        print 'COMPLETE ({}s)'.format(time.clock() - self.now)

    def display_results(self):
        for i, result in enumerate(self.results):
            print result
            if i > 10: break
        print 'There were {} successes in {} metagenerations ({}s)'.format(
               self.num_complete, self.generations, time.clock() - self.now)
        print 'DNAs (distinct, sorted by completion time):'
        prev_dna = {}
        for i, dna in enumerate(self.best_dnas):
            if dna == prev_dna:
                continue
            print '{}. {}'.format(i, dna)
            if i > 10: break
            prev_dna = dna

    def select(self):
        """
        1. Assign scores (fitness)
        2. Normalize / accumulate to form a probability distribution
        """
        weights, inverse_weights = [], []
        for metamonkey in self.metamonkeys:
            fitness = self.evaluate_fitness(metamonkey)
            weights.append(fitness)
            try:
                inverse_weights.append(1/fitness)
            except ZeroDivisionError:
                # TODO improve this
                inverse_weights.append(10000000000)
        self.cumdist = list(gmutils.accumulate(weights))
        self.invcumdist = list(gmutils.accumulate(inverse_weights))

    def reproduce(self):
        """
        1. Draw two parents,
        2. Crossover: create a 'child' by combining DNA of the parents
        3. Mutation: mutate childs DNA based on a given probability
        4. Replace random poor fitness monkey with new child
        TODO: find a way to add two dictionaries together....
        """
        #children = list()
        print list(['birthing...                                          \r',
                    'gestating...                                         \r'])\
                    [(int(floor(np.random.random()*2)))],
        for i in xrange(0, int(self.max_pop * self.birth_rate)):
            # Draw parents from probability distribution:
            father, mother = self.metamonkeys.get(bisect.bisect(self.cumdist, 
                                    np.random.random() * self.cumdist[-1])), \
                             self.metamonkeys.get(bisect.bisect(self.cumdist, 
                                    np.random.random() * self.cumdist[-1]))
            # Recombination
            try:
                new_dna = evolution.reproduce(evolution.meosis(father.dna), 
                                        evolution.meosis(mother.dna))

            except Exception:
                print 'father dna: {} mother dna: {}'.format(father.dna, 
                                                             mother.dna)
                raise
            seed = evolution.mutate(new_dna, self.mutation_rate, 
                                    self.mutation_significance)
            # Birth & mutation:
            child = MetaMonkey(self.phrase, **seed)
            #children.append(child)
            # Draw against the inverse probability distribution for a monkey
            # nwith a relatively lower fitness:
            senior_pos = np.random.random() * self.invcumdist[-1]
            senior = self.metamonkeys.get(bisect.bisect(self.invcumdist, 
                                                        senior_pos))
            # Senior may die naturally, otherwise child only replaces senior
            # if it has a higher fitness:
            if np.random.random() < self.mortality_rate or \
                                 self.evaluate_fitness(child) >= senior.fitness: 
             self.metamonkeys[
                           bisect.bisect(self.invcumdist, senior_pos)-1] = child
        #self.monkeys = children
        #print ''

    def evaluate_fitness(self, metamonkey):
        """
        Assign a score.
        # TODO COULD DO SIMULATED ANNEALING! by doing 1/gen. is it though?
        """
        avg_score = metamonkey.get_avg_score()
        found = int(metamonkey.found)
        gen = metamonkey.generation
        metamonkey.fitness = avg_score + found + gen
        #metamonkey.fitness = (avg_score + found) * 1/gen
        # Update average score:
        n = len(self.metamonkeys)
        self.avg_score = (avg_score + self.avg_score * n)/(n + 1)
        return metamonkey.fitness


class MetaMonkey(object):
    """
    A metamonkey defines an entire evolutionary sequence with unique parameters.

    Also contains stats such as number of generations to complete, average score
    """
    def __init__(self, phrase, **seed):
        if not seed:
            raise Exception('No seed was given!')
        self.phrase = phrase
        self.dna = seed
        self.env = Environment(self.phrase, **self.dna)
        self.found = False
        self.generation = 0
        self.scores = list()
        self.string = None
        self.fitness = float()
        self.elapsed_time = 0

    def evolve(self):
        """
        Single evolutionary hop.
        """
        if self.found:
            return True
        else:
            start = time.clock()
            self.env.select()
            for monkey in self.env.monkeys:
                print 'subgen: {} : phrase: {}: score: {}       \r'.format(
                                      self.generation, monkey, monkey.fitness),
                self.scores.append(monkey.fitness)
                if monkey.string == self.phrase:
                    self.elapsed_time += time.clock() - start
                    self.found = True
                    self.string = monkey.string
                    break
            if not self.found:
                self.env.reproduce()
                self.generation += 1
                return False
            self.elapsed_time += time.clock() - start
        print

    def get_avg_score(self):
        if sum(self.scores) is 0: return 0
        return np.mean(self.scores)


if __name__=='__main__':
    print 'Initializing MetaMonkeys'
    parser = argparse.ArgumentParser(description='MetaMonkeys v1')
    parser.add_argument('phrase', action='store', help='phrase to determine', 
                        type=str, nargs='?', default=PHRASE)
    parser.add_argument('max_pop', action='store', type=int, nargs='?',
                        default=META_MAX_POP, help='maximum population size')
    parser.add_argument('mutation_rate', action='store', type=float, nargs='?',
                        default=META_MUTATION_RATE, 
                        help='likelihood of random changes in DNA')
    parser.add_argument('mutation_significance', action='store', type=float, 
                        nargs='?', default=META_MUTATION_SIGNIFICANCE, 
                        help='degree of random change in DNA')
    parser.add_argument('birth_rate', action='store', type=float, nargs='?',
                        default=META_BIRTH_RATE, help='likelhood of births')
    parser.add_argument('mortality_rate', action='store', type=float, nargs='?',
                        default=META_MORTALITY_RATE, help='likelhood of deaths')
    args = parser.parse_args(sys.argv[1:])
    seed = {'mortality_rate':MORTALITY_RATE,
            'mutation_rate':MUTATION_RATE,
            'birth_rate':BIRTH_RATE,
            'max_pop':MAX_POP}
    kwargs = {'phrase':args.phrase,
              'seed':seed,
              'max_pop':args.max_pop,
              'mutation_rate':args.mutation_rate,
              'mutation_significance':args.mutation_significance,
              'birth_rate':args.birth_rate,
              'mortality_rate':args.mortality_rate}
    universe = Universe(**kwargs)
    try:
        universe.evolve()
    except KeyboardInterrupt:
        pass
    finally:
        universe.display_results()