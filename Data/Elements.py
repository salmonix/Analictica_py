import re
import math
from copy import copy

from NLP.Tokenizers import Tokenizer, Sentencer
from NLP.Filters import Stopword

from Modules.Abacus import entropy,probability

class Elements(object):
    """Object containing obj.tokens and obj.texts with some additional convenience methods on the top."""

    def __init__(self, sentencer, tokenizer, language):
        self.sentencer = Sentencer( sentencer, language )
        self.tokenizer = Tokenizer( tokenizer, language )

        self.tokens = Tokens()
        self.texts = Text()
        self.active = 'tokens'

    def process_datastring( self, title, data ):
        sentences = self.sentencer.process(data)
        for s in sentences:
            s = '_head_ ' + s # we add the head element. maybe we should take it from Tokens.tokens[0]
            tokens = self.tokenizer.get_tokens(s)
            self.add_data( title, tokens )

    def add_data(self, source, tokenlist ):
        """Convenience method to process a sentence into the text and token containers."""
        self.texts.add_text( source )
        idx = self.tokens.add_token(tokenlist) 
        self.texts.add_token_ids( idx )

    def activate(self, slot):
        if hasattr(self,slot) and slot != 'active':
            self.active = slot
        else:
            raise ValueError(slot + ' is not attribute of the Elements instance.')



class Tokens(object):
    """ Container for the tokens, the nodes. Token container is not optimal for deletion. """
    def __init__( self ):
        """The initial token is _head , which is the head of a sequence."""
        self.active = []
        self.slots = ['hidden']
        self.idx = 0
        self.no_of_tokens = 1
        self.tokens = [ {'name' : '_head_', 'freq' : 0, 'idx' : 0, 'colloc' : [] } ]  # token id ->{token_obj}
        self.names = { '_head_': 0 }   # name -> id TODO: lookup using trie
        self.calculation_cache = {} # this is to store the last values of calculations, like entropy or probability
        # this is a copy of the first token. 'Recalc': non existing or differs from the first calculation.

    def add_token( self, data ):
        """ Takes a string or list of strings ( tokens ) and stores in the tokenlist. Returns the index number(s) for the token. """
        if isinstance(  data, str ): # add a string - obsolete
            return self._add_token( data )
        elif isinstance( data, list ): # add a list of strings
            idxs = []
            for i in data:
                idxs.append( self._add_token( i ) )
            return idxs

    # TODO: here we should implement the case when a token is a superclass
    # because it may change the number of tokens -> I mean ontological solution, graph etc.
    # the way we use self.idx to calculate probability should change to a 'states' attribute later
    # that can be modified according to the parent categories
    def _add_token( self, name, parent={}, children={} ):
        if  name in self.names :     # token exists
            token = self.names[ name ]
            self.freq_incr( token )
            return self.tokens[ token ]['idx']

        # new token hash is made here
        else:
            self.idx += 1
            self.tokens.append( {'name' : name, 'freq' : 1, 'idx' : self.idx } )
            self.names[name] = self.idx
            return self.idx

    def get_token( self, token ):
        """Gets a token_id  ( index ) -> returns a token """
        return self.idx( token_id )

    def freq_incr( self, token, num = 1 ):
        if type(token) is str:
            token = self.names[token]
        
        self.tokens[token]['freq'] = self.tokens[token]['freq'] + num
        return self.tokens[token]['freq'] 

    # ###############################################################
    # these are functions acting on the tokens extending the core functionality
    # in future these may go into a helper module/class or so

    def order(self, by='freq' ):
        """Orders the tokens by an attribute and returns the [ ids ]."""
        if not self.tokens[-1][by]:
            raise ValueError( 'no attribute as ' + by )

        s = sorted( self.tokens, key = lambda x : ( x[ by ] ) )
        ret = []
        for i in s:
            ret.append( i['idx'] )
        return ret
    
    # ( self )->( self )
    def calculate_probability(self):
        if not 'p' in self.tokens[-1] or self.calculation_cache['p'] != probability(self.idx, self.tokens[-1] ):
            for i in self.tokens:
                i['p'] = probability(self.idx, i['freq'])
            self.make_unchanged()
        

    # ( self )->( self )
    def add_entropy(self, algo ):
        self.calculate_probability()

        if algo == 'shannon':
            entr = entropy(algo)
        else:
            raise ValueError( algo + ' is not implemented ')
        if not algo in self.tokens[-1] or self.calculation_cache[algo] != entr( self.tokens[-1] ):
            for t in self.tokens:
                t[algo] = entr(t)
        self.make_unchanged()

    def make_unchanged(self):
        self.calculation_cache = copy( self.tokens[-1] )


class Text(object):
    """Text container: stores the text transformed into sequences of token index numbers."""
    # TODO: in case of lots of texts it should be optimized
    def __init__(self):
        self.text={}
        self.active=''

    def add_text(self, source):
        """Start a new text unit."""
        if source in self.text:
            return self.text[source]

        self.text[source] = []
        self.active = source

    def add_token_ids(self,idxs):
        self.text[ self.active ].append( idxs )

    def get_text_by_title(self,title=[]):
        """Returns a title, text list tuple for the given text titles. If nothing is passed returns for all."""
        if title == []:
            title = self.text.keys()
            for t in title: # this is each sentence list
                yield (t, self.text[t])

    def get_sentences(self):
        for i in self.text.values():
            for s in i:
                yield s
