import math
from numpy import array, zeros
from copy import copy

# because it functions over the tokens it should be somehow cleverly incorporated ( I do not mean it is clever )

# XXX not necessary maybe
def entropy(name):
    if name == 'shannon':
        return shannon
    raise ValueError(name + ' is not a defined method')

def shannon(token, S):
    try:
        p = token['freq'] / S
        return -1 * p * math.log(p, 2)
    except:
        raise ValueError

def probability(S, freq):
    freq = float(freq)
    return 1 / (S / freq)


    def conditional_probability(A, B, S, on='co_occurrence'):  # on: the type of co-occurrence
        A['freq'] / S * A[ B[on] ]

def independent_joined_probability(A, B, S):
    return (A['freq'] * B['freq']) / math.pow(S, 2)
