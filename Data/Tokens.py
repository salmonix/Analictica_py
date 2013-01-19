import re
import NLP.Tokenizer

class Tokens:
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