"""
This file defines utility functions for geneticmonkeys project.
"""

from operator import add

__author__ = 'Yazan Obeidi'
__copyright__ = 'Copyright 2016, Yazan Obeidi'
__license__ = 'GPLv3'
__version__ = '0.0.2'
__maintainer__ = 'Yazan'
__email__ = 'yazan.obeidi@uwaterloo.ca'
__status__ = 'development'

def accumulate(iterable, func=add):
    """
    Generator of histogram bin style accumulation.
    IE accumulate([1,2,3,4,5]) --> 1 3 6 10 15 (addition)
    """
    it = iter(iterable)
    try:
        total = next(it)
    except StopIteration:
        return
    yield total
    for element in it:
        total = func(total, element)
        yield total

def hamming_distance(str1, str2):
    """
    Hamming string distance formula.
    """
    return sum(itertools.imap(str.__ne__, str1, str2))

def merge_dicts(*args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dic in args:
        result.update(dic)
    return result

class GMList(list):
    """
    Wrapper that allows to return a default value if index is greater than len.
    """
    def get(self, index, default=None):
        return self[index] if len(self) > index else default or self[index-1]