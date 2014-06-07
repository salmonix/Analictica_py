from pprint import pprint
from Crypto import SelfTest
from scipy import sparse


class Universe(object):

    """Universe contains all the states of the elements and their absolute attributes like frequency and co-occurrence.
    Regardless our point of wiev the elements in the Universe are full.""" 
    
    co_occurrences = {} # must be sparse array, let's use scipy now.
    tokens = []   # a simple id -> token lookup. at the moment this is not deletion friendly.
    names = {}    # a name -> id lookup. This lookup might be optimised, but we need a two way lookup
    idx = 0

    @property
    def element_size(self):
        return len(Universe.tokens)

    def add_token(self, name = ''):
 
        # block: check for existing token, increment it and return
        token = object
        try:
            token = Universe.names[name]
            token.freq_add(1)
            return token
        except:
            idx = len(Universe.tokens) + 1
            token = Token(name, idx)
            Universe.tokens.append(token)
            Universe.names[name] = ( token, idx )

    def add_tokenlist(self, data):
        """ Takes a list of tokens and stores them the tokenlist instance. Returns the list of tokens. """

    def get_token(self, idx):
        """Gets a token_id  ( index ) -> returns a token """

        return Universe.idx(idx)

    def freq_add(self, idx, num=1):
        
        token = None
        try:
            token = Universe.tokens[idx]
        except:
            token = Universe.names[idx]  # get the id

        if not token:
            raise ValueError( "I can not find the token with ID". idx) # it might be too strict. what about hidden elements?
            
        token.freq = token.freq + num 
        return token
    
    def get_token_names(self,names):
        return Universe.names[names]

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

    def co_occurrence(self,A):    
        return Universeco_occurrence[A.idx]



class View(object):
    """What is if we create a helper 'View' object to cache the main result of some calculations? """
    pass



class Token(Universe):
    """The Token class, with some philosophical notes.
    Now, the current attempt says that a token is a minimal element. The Universe contains all the elements.
    For practical reasons the Universe also reflects our perspective - in this case with the 'view' element. 
 
    Let's say that there is an explicite relation: 'a' is connected to 'b' some way, for example: 'a' is_a 'b'. 
    The other is 'fuzzy', non directed relation. These are more a kind of probabilistic relations to the 
    elements beyond the explicite relations in the given concept space. What does it mean?
    If 'a' element is associated with 'b' as an is_a relationship, then their probability does not count and the 
    'distance' of the two tokens are constantly 0 through the inheritance tree upwards. 
    However, if that association is non-existant in the is_a graph, then we still can ask if 'a' is_a 'c' ? 
    Now, the answer lies if 'c' is in the probabilistic vicinity of some 'b'... Say, 'yes, something close (75%).
    I guess this kind of behaviour can be detected daily.
    
    Some further note:
        the Token is responsible for its elements. However, when I need a property of a node I ask the node.
        So, the node must know its possible container to callibrate its frequency data to the actual state of
        the engine ( the perspective ). That means X indexing.
    
    """
    
    """Class variable and method declarations"""
    """ What do I want here? What about multiple inheritance? 
    A assoc. B, A2 assoc. B, does it mean that they must know about the universe? Where should they get their position? 
    I guess from Assoc. So, it has nothing to do with universe. However, Universe should know about the objects that are visible to 
    it ?"""
    
    
    _lookup = {}
    
    __slots__ = ('active', 'idx', 'name', 'freq', 'associates' )
    
    c = 0
    for i in __slots__:
        _lookup[i] = c
        c += 1
    
    def freq_add(self, num=1):
        self.freq += num

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
