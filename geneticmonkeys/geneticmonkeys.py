"""
The goal of this script is to produce a user-provided string by breeding
generations of evolutionary objects named Monkeys.
"""

import argparse
import sys
import random
import numpy as np
from Levenshtein import distance
import bisect
import string
import time
import math

import gmutils

__author__ = 'Yazan Obeidi'
__copyright__ = 'Copyright 2016, Yazan Obeidi'
__license__ = 'GPLv3'
__version__ = '0.0.2'
__maintainer__ = 'Yazan'
__status__ = 'development'

MAX_POP = 1500
MUTATION_RATE = 0.17
BIRTH_RATE = 1
MORTALITY_RATE = 0.01
STRING_SET = string.letters + ' ' + string.punctuation + string.digits

class Environment(object):
    """
    Environmental Goals: evaluate fitness, selection, and 
    variation & heredity through reproduction.
    """
    def __init__(self, phrase, max_pop, mutation_rate, 
                                        mortality_rate, birth_rate):
        self.phrase = phrase
        self.top_score = self.evaluate_fitness(Monkey(string=self.phrase))
        self.size = len(phrase)
        self.max_pop = int(max_pop)
        self.mutation_rate = float(mutation_rate)
        self.mortality_rate = float(mortality_rate)
        self.birth_rate = float(birth_rate)
        self.monkeys = gmutils.GMList()
        self.top_phrase = ''
        self.top_fitness = 0
        self.generation_number = 1
        #self.taboo = list()
        print 'Spawning geneticmonkeys "{p}" [pop: {n} mu: {mu} '\
                'mort: {m} birth: {br} sym: {sym}]            \r'.format(
                p=self.phrase, n=self.max_pop, 
                m=str.format('{0:.3f}', self.mortality_rate),
                mu=str.format('{0:.4f}', self.mutation_rate), 
                br=str.format('{0:.4f}', self.birth_rate),
                sym=len(STRING_SET)),
        if __name__=='__main__':
            print ''
        for i in xrange(0, self.max_pop):
            self.monkeys.append(Monkey(size=self.size))

    def evolve(self):
        found = False
        now = time.clock()
        while not found:
            self.select()
            for monkey in self.monkeys:
                monkey.age += monkey.age
                t = time.clock() - now
                print 'gen. {g} : "{p}" : {s} top: {w} ({t}s)    '\
                      '    \r'.format(g=self.generation_number, p=monkey, 
                       s=str.format('{:.2E}', monkey.fitness), 
                       w=(self.top_phrase, '{}/{}'.format(
                       str.format('{:.2E}', self.top_fitness), 
                       str.format('{:.2E}', self.top_score))),
                       t=str(t)[:6]),
                if monkey.string == self.phrase:
                    t = time.clock() - now
                    print ''
                    print 'PHRASE FOUND in generation {} ({}s)'.format(
                                            self.generation_number, t)
                    found = True
                    return
            self.reproduce()
           # self.taboo = list()
            self.generation_number += 1

    def reproduce(self):
        """
        1. Draw two parents,s
        2. Crossover: create a 'child' by combining DNA of the parents
        3. Mutation: mutate childs DNA based on a given probability
        4. Replace random poor fitness monkey with new child
        """
        for i in xrange(0, int(self.max_pop * self.birth_rate)):
            # Draw parents from probability distribution:
            father, mother = self.monkeys.get(bisect.bisect(self.cumdist,
                                    np.random.random() * self.cumdist[-1])), \
                             self.monkeys.get(bisect.bisect(self.cumdist, 
                                    np.random.random() * self.cumdist[-1]))
            # Recombination, birth & mutation:
            new_dna = ''.join([father[int((self.size)/2):], 
                               mother[:int(self.size/2)]])
            child = Monkey(string=new_dna)
            child.mutate(self.mutation_rate)
            #while np.random.random() < 0.7 or child.string in self.taboo:
                #print 'checking taboo list...                               '\
                #'                        \r',
            #    child.mutate(self.mutation_rate)
            # Draw against the inverse probability distribution for a monkey
            # nwith a relatively lower fitness:
            senior_ = np.random.random() * self.invcumdist[-1]
            senior = self.monkeys.get(bisect.bisect(self.invcumdist, senior_))
            # Child may die naturally, otherwise child only replaces senior
            # iff it has a higher fitness:
            if np.random.random() < self.mortality_rate or \
                 self.evaluate_fitness(child, self.generation_number) >= \
                 self.evaluate_fitness(senior, self.generation_number):
                try:
                    self.monkeys[bisect.bisect(self.invcumdist, 
                                               senior_)] = child
                except IndexError:
                    # to account for bisect.bisect 'off by one'
                    self.monkeys[-1] = child
                finally:
                    pass#self.taboo.append(new_dna)

    def select(self):
        """
        1. Assign scores (fitness)
        2. Normalize / accumulate to form a probability distribution
        """
        weights, inverse_weights = [], []
        for monkey in self.monkeys:
            monkey.fitness = self.evaluate_fitness(monkey, 
                                    self.generation_number)
            #self.taboo.append(monkey.string)
            # Keep track of top monkey:
            if monkey.fitness > self.top_fitness:
                self.top_phrase = monkey.string
                self.top_fitness = monkey.fitness
            weights.append(monkey.fitness)
            try:
                inverse_weights.append(1/monkey.fitness)
            except ZeroDivisionError:
                # TODO improve this
                inverse_weights.append(1000)
        self.cumdist = list(gmutils.accumulate(weights))
        self.invcumdist = list(gmutils.accumulate(inverse_weights))

    def evaluate_fitness(self, monkey, gen=1):
        """
        Assign a score with minimal assumptions of the encoding. Currently uses:
        matches = [# of strict char matches (case sensitive) ]
        fuz = fuzzy matches
        lev = levenshtein distance
        age = monkeys age (in number of genetic evolutions)
        >> fitness = (matches + fuz)^(lev/age)
        """
        # how many matches we have:
        strict_matches = sum([1 if letter in self.phrase[i] \
                             else 0 for i, letter in enumerate(monkey.string)])
        letters = list(self.phrase)
        fuzzy_matches = len([letters.remove(letter) for letter \
                                        in monkey.string if letter in letters])
        # levenshtein distance:
        levenshtein_distance = distance(monkey.string,self.phrase)
        levenshtein_score = (len(self.phrase) - levenshtein_distance)
        #correct_letters = len([letters.remove(letter) for letter in \
                               #monkey.string if letter in letters])
        #fitness = (levenshtein_score) ** ((strict_matches+fuzzy_matches) / monkey.age)
        #fitness = (levenshtein_score) * (strict_matches ** (fuzzy_matches * 1/monkey.age))
        #fitness = (levenshtein_score * (monkey.age/gen) + strict_matches) ** fuzzy_matches
        #fitness = ((levenshtein_score + strict_matches) + fuzzy_matches) * (monkey.age/gen) 
        # The following seems to actually work quite well, but I do not like the "hack" nature of it
        """
        if len(self.phrase) < 7:
            fitness =  strict_matches+gen*fuzzy_matches/(monkey.age)+levenshtein_score
        else:
            fitness = strict_matches + fuzzy_matches + levenshtein_score
        """
        fitness = (len(self.phrase)*fuzzy_matches)/monkey.age + strict_matches * levenshtein_score
        return fitness

    def _evaluate_fitness(self, monkey):
        """
        Previous version. Assign a score. Currently uses:
        fitness = # of char matches (case sensitive) * levenshtein distance
        """
        matches = sum([1 if letter in self.phrase \
                                            else 0 for letter in monkey.string])
        levent_score = (len(self.phrase) - distance(monkey.string, self.phrase))
        fitness = matches * levent_score
        return fitness
        #return levent_score * sum([1 if char in self.phrase[i] else 0 for i, char in \
                                                      #enumerate(monkey.string)])

    def get_best_monkey(self):
        """
        Returns tuple of string, fitness of monkey with greatest fitness.
        """
        top_monkey_fitness = 0
        top_monkey_string = None
        for monkey in self.monkeys:
            if monkey.fitness >= top_monkey_fitness:
                top_monkey_fitness = monkey.fitness
                top_monkey_string = monkey.string
        return top_monkey_string, str.format('{:.2E}', top_monkey_fitness)


class Monkey(object):
    """
    Monkey is the object we will be evolving. It genotype and phenotype are the
    same: self.string.
    """
    def __init__(self, size=None, string=None):
        self.string = string or self.seed(size)
        self.fitness = 0
        self.age = 1

    def __repr__(self):
        return self.string

    def __getitem__(self, sliced):
        return self.string[sliced]

    def seed(self, size=1, chars=STRING_SET):
        """
        Initial seed population random DNA generation.
        """
        return ''.join(random.choice(chars) for x in xrange(size))

    def mutate(self, rate, chars=STRING_SET):
        """
        Perform a char swap, for all characters in DNA, with likelihood 'rate'.
        """
        new_string = ''
        for letter in self.string:
            new_string += random.choice(chars) \
                            if np.random.random() <= rate else letter
        self.string = new_string


if __name__ == '__main__':
    print 'Initializing...'
    parser = argparse.ArgumentParser(description='Genetic Monkeys v1')
    parser.add_argument('phrase', action='store', help='phrase to determine', 
                        type=str, nargs='?', default='cat')
    parser.add_argument('max_pop', action='store', type=int, default=MAX_POP,
                        help='maximum population size', nargs='?')
    parser.add_argument('mutation_rate', action='store', type=float, nargs='?',
                        default=MUTATION_RATE, 
                        help='likelihood of random changes in DNA')
    parser.add_argument('birth_rate', action='store', type=float, nargs='?',
                        default=BIRTH_RATE, help='likelhood of births')
    parser.add_argument('mortality_rate', action='store', type=float, 
                        nargs='?', default=MORTALITY_RATE, 
                        help='likelhood of deaths')
    args = parser.parse_args(sys.argv[1:])
    kwargs = {'phrase':args.phrase,
              'max_pop':args.max_pop,
              'mutation_rate':args.mutation_rate,
              'birth_rate':args.birth_rate,
              'mortality_rate':args.mortality_rate}
    Earth = Environment(**kwargs)
    try:
        Earth.evolve()
    except KeyboardInterrupt:
        print ''
        print 'Top monkey alive: {}'.format(Earth.get_best_monkey())
        #print 'taboo length: {}'.format(len(Earth.taboo))