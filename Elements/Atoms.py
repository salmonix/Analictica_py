from math import log

class Atoms(object):
    """Container for the tokens, the nodes. Token container is not optimal for deletion because it maintains an array."""

    def __init__(self):
        """The initial token is _head , which is the head of a sequence."""

        self.active = []
        self.idx = 0
        self.no_of_tokens = 1
        self.tokens = []  # token id ->{token_obj}
        self.names = {}  # name -> id TODO: lookup using trie
        self.S = 1.0  # helps to fix most calculations as floats

    # add_tokenlist
    def add_tokenlist(self, data):
        """ Takes a list of tokens and stores them the tokenlist instance. Returns the list of tokens. """

        tks = []
        for i in data:
            tks.append(self.add_token(i))
        return tks

    def add_token(self, name, parent={}, children={}):

        self.S += 1

        if  name in self.names :  # token exists
            idx = self.names[ name ]
            self.freq_add(idx)
            # print ('exists: ' + name)
            return self.tokens[idx]

        else:  # new token hash is made here
            self.tokens.append(Atom(name, self.idx, self))
            self.names[name] = self.idx
            # print ('not exists : ' + name)
            idx = self.idx
            self.idx += 1
            return self.tokens[-1]

    def get_token(self, idx):
        """Gets a token_id  ( index ) -> returns a token """

        return self.idx(token_id)

    def freq_add(self, idx, num=1):
        if type(idx) is str:
            token = self.names[idx]  # get the id

        self.tokens[idx].freq_add(num)
        return self.tokens[idx].freq


class Atom(object):
    """Token object. The co_occurrence is a matter of definition."""
    __slots__ = ('co_occurrence', 'name', 'freq', 'idx', 'S', 'attribute', 'value')
    def __init__(self, name, idx, parent, freq=1.0):
        self.value = name
        self.idx = idx
        self.freq = freq
        self.co_occurrence = {}
        self.S = parent
        self.attribute = ()

    def freq_add(self, num=1):
        self.freq += num

    @property
    def name(self):
        return self.value

    @property
    def Space(self):
        """The probability space."""
        return self.S.S

    @property
    def shannon(self):
        """Shannon entropy for the token: -p(A)*log2( p(A) ) 
        If frequency is not set it returns 1.0."""

        if self.freq != 0:
            try:
                # print ('FREQUENCY: ' + str(self.freq) + ' SPACE: ' + str(self.Space))
                p = self.freq / self.Space
                # print ('Probability: ' + str(p))
                # print ('Shannon: ' + str(-1 * p * log(p, 2)))
                return -1 * p * log(p, 2)
            except:
                raise ValueError('calculation went wrong')
        else:
            return 1.0

    @property
    def IC(self):
        """Information content for the token: -log2( p(A) ) 
        If frequency is not set it returns 1.0."""
        if self.freq != 0:
            try:
                # print ('FREQUENCY: ' + str(self.freq) + ' SPACE: ' + str(self.Space))
                p = self.freq / self.Space
                # print ('Probability: ' + str(p))
                # print ('Shannon: ' + str(-1 * p * log(p, 2)))
                return -1 * log(p, 2)
            except:
                raise ValueError('calculation went wrong')
        else:
            return 1.0


    @property
    def probability(self):
        """Standard probability: freq/Space"""

        return self.freq / self.Space

    def conditional_probability(self, B):
        """Conditional probability on B: p(A&B)/P(B)"""
        if B.idx in self.co_occurrence:
            return self.freq / self.Space * self[ B.co_occurrence[ B.idx ] ]
        else:
            return 0.0

    def PMI(self, B):
        """Pointwise Mutual Information PMI(A|B) = p(A&B) / p(A)xp(B)"""
        # print ('CO_OCC:' + str(self.co_occurrence))
        if B.idx in self.co_occurrence:
            return log(2, (self.co_occurrence[B.idx] * self.Space) / (self.freq * B.freq))
        else:
            return 0.0

    def PMI_with(self, B):
        return self.PMI(B)
