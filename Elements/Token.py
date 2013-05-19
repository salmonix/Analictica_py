from math import log
from pprint import pprint
# from sets import frozenset  # a python3 type.

class Token(object):
    """The Token class, with some philosophical notes. 
    The token is a Janus-faced thing. It can either be an element, that
    has certain 'atomic' properties - eg. probability related to the given probability space -, or
    as a set of tokens, a TokenList, that itself represent a probability space for those elements that it 
    contains. This is simply a matter of perspective or invocation. It is important to note, that it is possible,
    that one particular element belongs to multiple TokenLists in different spaces... 
    The relations of the Tokens is twofold, and here is one possible modell, that can be 
    evaluated with this structure.
    Let's say that there is an explicite relation: 'a' is connected to 'b' some way, for example: 'a' is_a 'b'. 
    The other is 'fuzzy', non directed relation. These are more a kind of probabilistic relations to the 
    elements beyond the explicite relations in the given concept space. What does it mean?
    If 'a' element is associated with 'b' as an is_a relationship, then their probability does not count and the 
    'distance' of the two tokens are the steps of reaching from one point to the other. We predeclared a concept and 
    However, if that association is non-existant in the is_a graph, then we still can ask if 'a' is_a 'c' ? 
    Now, the answer lies if 'c' is in the probabilistic vicinity of some 'b'... Say, 'yes, something close (75%)."""

    __slots__ = ('active', 'idx', 'tokens', 'names', 'S', 'freq', 'co_occurrence', 'attribute', '_associates', 'parent')
    _lookup = {}
    c = 0
    for i in __slots__:
        _lookup[i] = c
        c += 1

    def __init__(self, **kwargs):
        """The container aspect of the Token class. The methods here are acting on the internal
        list attribute and on possibly multiple elements in it."""
        # container attributes
        defaults = { 'active':[],
                     'idx': 0,
                     'tokens': [],
                     'names':{},
                     'S':1.0,
                     'name':name,  # atomics
                     'parent': Root(),
                     'freq':1.0,
                     'co_occurrence':{},
                     'attribute':{},
                     '_associates': {} }

        for k, v in defaults.iteritems():
            try:
                if k in kwargs:
                    self.__slots__[_lookup[k]] = kwargs[k]
                else:
                    self.__slots__[_lookup[k]] = v
            except:
                raise Error('Something is wrong')


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
            self.tokens.append(Element({'name':name, 'idx' : self.idx, 'parent' : self }))
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

    # XXX: this is the method that prevents me from using __slots__.
    # If I would use a hash lookup for the slots, it could work.
    def get_subset_by_attribute(self, kwarg):
        """Example: 
            elements.get_subset_by_attribute({ 'decorator' : 'hidden' })
            elements.get_subset_by_attribute({ 'name' : [ ... ] })
            elements.get_subset_by_attribute({ 'PMI' : lambda x : x < 0.14 and x > 6.21 })
            can be iteratively 
        """
        subset = self.tokens
        for attr, constraint in kwarg.items():
            attr = _lookup[attr]
            # pprint(subset[0].__dict__)
            if hasattr(constraint, '__iter__'):
                print('ITER in SUBSET')
                constraint = set(constraint)
                subset = [ i for i in subset if i.__slots__[attr] in constraint ]

            elif type(constraint) == 'function':
                subset = [ i for i in subset if constraint(i.__slots__[attr]) ]

            else:
                try:
                    subset = [ i for i in subset if i.__slots__[attr] == constraint ]
                except:
                    raise ValueError('Constraint is neither iterable, nor scalar, nor lambda.' + constraint)

        return subset


    """The atomic aspects of the Token class. These methods are acting on the values of a single element. 
    The co_occurrence is a matter of definition.
    S : the no of elements in the probability space
    decorator: a special attribute of the element, eg. stopword
    attribute: custon attributes"""
    def freq_add(self, num=1):
        self.freq += num

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

        """Associate functions: Associates act as a kind of edge or conditional behaviour. These allow to build a complex fuzzy graph
        of elements, adding instance method to the instance.
        
        """

    # TODO: Put into associates behavioural class
    def associate(self, element, *args):
        """Recalls the associate self[attribute] to the given parameter."""

        if element:
            pass
        # associate can be: an other label, a method or a value.

    def make_associate(self, assoc, to_this):
        """The association can be an assignment or a rule ( method ). Eg.:
        self.associate( 'distance':'120') or
        self.associate('distance' : function() )"""
        if not hasattr(to_this, 'function'):
            new_func = lambda x : x

        setattr(self, assoc, to_this)


