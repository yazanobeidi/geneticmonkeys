"""
This file defines general numerical evolutionary computing functions.

    Copyright (C) 2016 Yazan Obeidi

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np

__author__ = 'Yazan Obeidi'
__copyright__ = 'Copyright 2016, Yazan Obeidi'
__license__ = 'GPLv3'
__version__ = '0.0.2'
__maintainer__ = 'Yazan'
__status__ = 'development'

def meosis(dna):
    """
    Reduces DNA by half for 'reproduction'. Really is 'Miosis I'
    Approach: divide values in two, will result in an average upon sex.
    :param: dna: dictionary containing gene and expression key value pairs
    :return: haploid: reduced (only 'half of') dictionary representation of DNA
    """
    if not dna:
        raise Exception('Empty DNA set was provided: {}'.format(dna))
    haploid = dict()
    for gene, expression in dna.iteritems():
        haploid[gene] = float(expression) / float(2)
    return haploid

def reproduce(haploid1, haploid2):
    """
    Assumes both haploids passed are identical, ie one doesn't have items
    the other has.
    :param: haploidX: reduced (only 'half of') dictionary containing gene and
    expression key value pairs
    :return: child_dna: combined version of haploids
    """
    if len(haploid2) is not len(haploid1):
        raise Exception('Unequal haploid lengths: {} vs {}'.format(haploid1,
                                                                   haploid2))
    child_dna = dict()
    for gene, expression in haploid1.iteritems():
        child_dna[gene] = float(expression) + float(haploid2[gene])
    return child_dna

def mutate(dna, rate, significance):
    """
    For each bit of dna, add (or subtract) a random proportion of itself.
    :param: dna: dictionary containing gene and expression key value pairs
    :param: rate: likelyhood a mutation will occur
    :param: significance: proportion magnitude
    :return: new_dna: potentially altered version of dna
    """
    new_dna = dna
    for gene, expression in dna.iteritems():
        expr = float(expression)
        mutation = expr + (expr * np.random.normal(scale=significance))
        if np.random.random() <= rate:
            new_dna[gene] = mutation
    if not new_dna:
        raise Exception('for some reason, mutation has created an empty DNA\n'\
                        'new_dna: {} \nold_dna: {}'.format(new_dna, dna))
    else:
        return new_dna