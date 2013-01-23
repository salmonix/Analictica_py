import re
import math

# I do not know if it is a great idea to put so much functionality here
class Elements(object):
    """Object containing obj.tokens and obj.texts with some additional convenience methods on the top."""

    def __init__(self):
        self.tokens = Tokens()
        self.texts = Text()
        self.active = 'tokens'

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


# TODO: decide on the interface. Perhaps asking for the texts and tokens object when
# those are acting separate, and writing the convenience methods here only. But that looks 
# awkward to make this module triple faced

class Tokens(object):
    """ Container for the tokens, the nodes. Token container is not optimal for deletion. """
    def __init__( self ):
        self.active = []
        self.slots = ['hidden']
        self.idx = 0
        self.no_of_tokens = 0
        self.tokens = []   # token id ->{token_obj}
        self.names = {}   # name -> id

    def add_token( self, data ):
        """ Takes a string or list of strings ( tokens ) and stores in the tokenlist. Returns the index number(s) for the token. """
        if isinstance(  data, str ): # add a string
            return self._add_token( data )
        elif isinstance( data, list ): # add a list of strings
            idxs = []
            for i in data:
                idxs.append( self._add_token( i ) )
            return idxs

    # here we should implement the case when a token is a superclass
    # because it may change the number of tokens
    def _add_token( self, name, parent={}, children={} ):
        if  name in self.names :     # token exists
            token = self.names[ name ]
            self.freq_incr( token )
            return self.tokens[ token ]['idx']

        # new token hash is made here
        else:
            self.tokens.append( {'name' : name, 'freq' : 1, 'idx' : self.idx } )
            self.names[name] = self.idx
            self.idx += 1
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
    # these are functions acting on the tokens but not inherently related to the class.
    # in future these may go into a helper module/class

    def order(self, by='freq' ):
        """ Orders the tokens by a numeric attribute and returns the [ ids ]."""
        s = sorted( self.tokens, key = lambda x : ( x[ by ] ) )
        ret = []
        for i in s:
            ret.append( i['idx'] )
        return ret

    def calculate_probability(self):
        for i in self.tokens:
            freq = float(i['freq'])
            p = 1/(self.idx/freq)
            i['p'] = p

    def add_entropy(self, algo ):
        if not 'p' in self.tokens[0]:
            self.calculate_probability()

        if algo == 'shannon_entropy':
            for t in self.tokens:
                p = t['p']
                t[algo] = -1*p*math.log(p,2)
        else:
            raise ValueError( algo + ' is not implemented ')




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

    def get_text(self,text=[]):
        """Returns a title, text list tuple for the given text titles. If nothing is passed returns for all."""
        if text == []:
            text = self.text.keys()
            for t in text: # this is each sentence list
                yield (t, self.text[t])
