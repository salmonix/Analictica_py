from math import log
import Token

class Links(Atoms):
    """Links are joined Atoms. Their name is a tuple, and knows the source Tokens instance to maintain its position in the graph."""

    def __init__(self, source):
        self.active = []
        self.idx = 0
        self.no_of_tokens = 1
        self.tokens = []  # token id ->{token_obj}
        self.names = {}  # name -> id TODO: lookup using trie
        self.S = 1.0  # helps to fix most calculations as floats
        self.source = source

    def add_tokenlist(self, data):
        """ Takes a list of links and stores them the Atomlist instance. Returns the index number(s) for the Atom. """

        idxs = []
        for i in data:
            idx = (self.add_token((i[0], i[1])))
            self.tokens[idx].link_PMI(i[2])

        return idxs

    def add_token(self, name, parent={}, children={}):

        self.S += 1

        if  name in self.names :  # token exists
            idx = self.names[ name ]
            self.freq_add(idx)
            # print ('exists: ' + name)
            return self.tokens[idx]

        else:  # new token hash is made here
            self.tokens.append(Link(name, self.idx, self))
            self.names[name] = self.idx
            # print ('not exists : ' + name)
            idx = self.idx
            self.idx += 1
            return self.tokens[-1]


class Link(Atom):
    """Links are Atoms, only differ that their name is a tuple and have some link specific attribute."""

    __slots__ = ('co_occurrence', 'name', 'freq', 'idx', 'S', 'attribute', 'value')
    def __init__(self, name, idx, parent, freq=1.0):
        self.value = name
        self.idx = idx
        self.freq = freq
        self.co_occurrence = {}
        self.S = parent
        self.attribute = ()

    @property
    def PMI(self):
        """Returns the PMI of the link elements."""
        (l, r) = self.value
        # print ('PMI:: ' + str(l.PMI(r)))
        return l.PMI(r)

    @property
    def name(self):
        """Returns the real names of elements that the link are composed of as a stringified tuple."""
        return (self.value[0].name, self.value[1].name)
