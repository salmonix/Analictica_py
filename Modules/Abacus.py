import math
from numpy import array, zeros
from copy import copy

# because it functions over the tokens it should be somehow cleverly incorporated ( I do not mean it is clever )

# XXX not necessary maybe
def entropy(name):
    if name == 'shannon':
        return shannon
    raise ValueError(name + ' is not a defined method')

def shannon(token):
    try:
        p = float(token['p'])
        return -1 * p * math.log(p, 2)
    except:
        raise ValueError

def probability(S, freq):
    freq = float(freq)
    return 1 / (S / freq)


def conditional_probability(Pa, Pb, S, on='co_occurrence'):  # on: the type of co-occurrence
    Pa['freq'] / S * Pa[ Pb[on]['idx'] ]

def independent_joined_probability(Pa, Pb, S):
    return (Pa['freq'] * Pb['freq']) / math.pow(S, 2)
