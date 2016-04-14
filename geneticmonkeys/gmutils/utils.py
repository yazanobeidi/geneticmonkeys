"""
This file defines utility functions for geneticmonkeys project.

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