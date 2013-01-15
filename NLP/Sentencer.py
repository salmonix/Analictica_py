import re
import nltk.data

# the punkt algorithm understands the pattern: ... VP
# the algorithm does not understand the pattern: , ... NP etc.
# I have not checked the abbreviations.
from nltk.tokenize import sent_tokenize

class Sentencer:
    # this is a factory like part. It may go into different factory classes if needed
    # these are preprocessing regexps.
    rm_noise = re.compile('\s+')
    normal_punct = re.compile('\.+[?!]*|[?!:]') # XXX it might be useful for syntactic analysis

    def __init__( self, sentencer='punct', language='english' ):

        languages=['english']
        if language in languages:
            self.language = language
        else:
            raise ValueError('Language "',langauge,'" not implemented')

        # initialize the sentencer
        sentencers=['punct']
        if sentencers.index[sentencer]:
            if sentencer == 'punct':
                sefl.sentencer = nltk.data.load('tokenizers/punkt/'.language.'.pickle')

        else:
            raise ValueError('Sentencer: "',sentencer,'" not implemented')

        self.data = []

    def process( self, string ):
        """ Takes a string and processes it. Returns a list of sentences"""

        # preparation
        e = self.data.pop()
        e = normal_punct( e )
        e = rm_noise.sub( ' ',e )
        # make a factory here using self.sentencer
        return self.sentencer.tokenize(e)
