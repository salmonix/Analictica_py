import re
import array


# I do not know if it is a great idea to put so much functionality here
class Elements(object):
    """Object containing obj.tokens and obj.texts with some additional convenience methods on the top."""

    def __init__(self):
        self.tokens = Tokens()
        self.texts = Text()
        self.active = 'tokens'

    def add_data(self, source, sentence ):
        """Convenience method to process a sentence into the text and token containers."""
        self.texts.text( source )
        self.texts.add_token_idx( self.token.add_token(tokens) )

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
        self.tokens = [{}]   # token id -> id, token
        self.names = {}   # name -> id

    def add_token( self, data ):
        """ Takes a string or list of strings ( tokens ) and stores in the tokenlist. Returns the index number(s) for the token. """
        if isinstance(  data, str ):
            return self._add_token( data )
        elif isinstance( data, list ):
            idxs = []
            for i in list:
                idsx.append( self._add_token( i ) )

    # here we should implement the case when a token is a superclass
    # because it may change the number of tokens
    def _add_token( self, name, parent={}, children={} ):
        if  self.names.has( name ): # token exists
            token = self.names[ name ]
            self.freq_in( token )

        # the token hash is made here
        else:
            self.tokens.append( {'name' : name, 'freq' : 1, 'idx' : self.idx } )
            self.names[name] = self.idx
            self.idx += 1

        return token.idx

    def get_token( self, token ):
        """Gets a token_id  ( index or name ) -> returns a token """
        return self.idxs( token_id )

    def order(self, by='freq' ):
        """ Orders the tokens by a numeric attribute. """
        tokens = self.tokens
        sorted_ids = sorted( self.idxs(), key = tokens[x][ by ] )
        indexed_list = self.idxs
        for i in sorted_ids:
            entity = indexed_list[i] # tuple of id, token, order value ( by )
            token = entity[1]
            self.__dict__[by][i] = ( entity[0], token, token._)

    def freq_incr( self, token, num = 1 ):
        freq = self.idxs[token]['freq']
        freq = freq+num


class Text(object):
    """Text container: stores the text transformed into sequences of token index numbers.
    """
    def __init__(self):
        self.text={}
        self.active=''

    def text(self, source):
        """Start a new text unit."""
        if self.text[source]:
            return self.text[source]

        self.text[source] = array.array('L') # we use long ints
        self.active = source

    def add_token_idx(self,idx):
         self.text[ self.active ].append(idx)

    def get_text(self,text=[]):
        """Returns a title, text_array tuple for the given text titles. If nothing is passed returns for all."""
        if text == []:   # this is perlish because we can make it an iterator on hash which might be better
            text = self.text.keys()
            for i in text:
                yield (i, self.text[i])
