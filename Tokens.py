input re

class Token_container:
    """ Container for the tokens, the nodes. Token container is not optimal for deletion. """
    def __init__( self ):
        self.active = []
        self.slots = ['hidden']
        self.idx = 0
        self.no_of_tokens = 0
        self.tokens = [{}]   # token id -> id, token
        self.names = {}   # name -> id


    def add_token( self, data ):
    """ Takes a string or list and creates a token. Returns the index number for the token. """
        if isinstance(  data, str ):
            self._add_token( data )
        elif isinstance( data, list ):
            map( self._add_token( name ), data )
               

    # here we should implement the case when a token is a superclass
    # because it may change the number of tokens
    def _add_token( self, name, parent={}, children={} ):
        if  self.names.has( name ): # token exists
            token = self.names[ name ]
            self.freq_in( token )
        
        # the token hash is made here
        else:  
            self.tokens.append.( {'name' : name, 'freq' : 1, 'idx' : self.idx } )
            self.names[name] = self.idx
            self.idx += 1

        return token.idx 

    def get_token( self, token ):
        """Gets a token_id  ( index or name ) -> returns a token """
        return self.idxs( token_id )

    def order(self, by='freq' ):
    """ Orders the tokens by a numeric attribute. """
        tokens = self.tokens
        sorted_ids = sorted( self.idxs(), key = x:( tokens[x][ by ]) )
        indexed_list = self.idxs
        for i in sorted_ids:
            entity = indexed_ list[i] # tuple of id, token, order value ( by )
            token = entity[1]
            self.__dict__[by][i] = ( entity[0], token, token._) 

    def freq_incr( self, token, num = 1 ):
        freq = self.idxs[token]{'freq'}
        freq = freq+num


# this is a container for the text converted into indices.
# basically this is a text matrix.
class Text_container:
    def __init__(self): 
        self.text=[] 
        self.pos=0

    def next_unit(self):
    # append only if the actual position is filled
        if self.text[ self.pos ] and len( self.text ):
            self.text.append([])
            self.pos  +=1 

    def prev_unit(self):
        self.pos -= 1

    def append_token(self,token):
        self.text[ self.pos ].append( token )
