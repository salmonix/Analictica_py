input re
from nltk.data import 

# the algorithm understands the pattern: ... VP
# the algorithm does not understand the pattern: , ... NP etc.
from nltk.tokenize import sent_tokenize

# this should go into the Tokenizer
from nltk.tokenize.punkt import PunktWordTokenizer


class Sentencer:
    # this is a factory like part. It may go into different factory classes if needed
    def __init__( self. sentencer='punct', la nguage='english' ):

        languages=['english']
        if languages.index[ language ]
            self.language = language
        else:
            raise ValueError('Language "',langauge,'" not implemented')

        sentencers=['punct']
        if sentencers.index[sentencer]
            self.sentencer = sentencer
        else:
            raise ValueError('Sentencer: "',sentencer,'" not implemented')

        self.data = []

    def add_text (self, string ):
        """ Piles up the string it receives"""
        self.data.append

    def process( self, processor='space' ): # it should be a factory 
        """ Takes a string and processes it. If string is not passed, 
        the previously stored data is processed. See: add_string method.
        This is not a really smart solution, but simpler at the moment than 
        building a state engine.
        """
        rm_noise = re.compile('\s+')
        normal_punct = re.compile('\.+[?!]*|[?!:]') # XXX it might be useful for syntactic analysis

        # preparation
        self.data.reverse() # we consume up the original data list
        Tokens = Token_container()
        Text = Text_container()
        while self.data:
            e = self.data.pop()
            e = normal_punct( e )
            e = rm_noise.sub( ' ',e )
            sen = sent_tokenize(e)
            # here we simply add it back and return. The tokenization may happen on a higher level using a 'state engine'
            for tok in sen:
                idx = Token_container.append_token(tok)
                Text_container.add_token(idx)

            Text_container.next_unit()
        return ( Tokens, Text )

