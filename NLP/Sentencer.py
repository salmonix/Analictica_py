import re
# from nltk.data import   # do I need it?

# the algorithm understands the pattern: ... VP
# the algorithm does not understand the pattern: , ... NP etc.
# I have not checked the abbreviations.
from nltk.tokenize import sent_tokenize

class Sentencer:
    # this is a factory like part. It may go into different factory classes if needed
    def __init__( self, sentencer='punct', language='english' ):

        languages=['english']
        if languages[ language ]:
            self.language = language
        else:
            raise ValueError('Language "',langauge,'" not implemented')

        sentencers=['punct']
        if sentencers.index[sentencer]:
            self.sentencer = sentencer
        else:
            raise ValueError('Sentencer: "',sentencer,'" not implemented')

        self.data = []

    def process( self, string ): # it should be a factory
        """ Takes a string and processes it. Returns a list of sentences"""

        rm_noise = re.compile('\s+')
        normal_punct = re.compile('\.+[?!]*|[?!:]') # XXX it might be useful for syntactic analysis
        # preparation
        e = self.data.pop()
        e = normal_punct( e )
        e = rm_noise.sub( ' ',e )
        return sent_tokenize(e)
