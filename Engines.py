from copy import copy
from Modules.Abacus import yuret_attraction

def get_engine(name, elements ):
    if name == 'trainee':
        return Trainee( elements )
    if name = 'tao':
        return Tao( elements )
    raise ValueError( name + 'is not implemented' )


class Trainee(object):
    """Learns fast, executes fast - but does not improve."""
    def __init__(self, elements): # here we should check if 'elements' is an Elements instance
        self.elements = elements
        self.stack = []
        # for fast lookup we alway take the lower element of the pair into the matrix as id
        # XXX: it is lazy and not memory effective but I have not time to think now.
        self.link_matrix = range( 0..elements.tokens.idx )

    # at this point I do not check crossing links or cycles, only negative values.
    def process_sentence( data ): # takes a sentence list
        data = copy(data)
        end = len(data)-1
        p = 1
        for p in p..0: # p = pointer
            
            head = data[p]
            for tail in p..end:



class Tao(object):
    """It learns always - the more it learns the slower it gets - but it comes with wisdom."""
    def __init__(self, elements):
        self.elements = elements
