import re
import nltk.data
from nltk.tokenize.punkt import PunktWordTokenizer
from nltk.tokenize import sent_tokenize # this is the regexp based tokenizer


class Tokenizer(object):
    def __init__(self, tokenizer,language, stopwords=None ):
        try:
            if tokenizer == 'PunktWord':
                self.tokenizer = PunktWordTokenizer()
        except:
            raise ValueError(tokenizer+" tokenizer not implemented" )

    def get_tokens(self,string):
        return self.tokenizer.tokenize(string)

class Sentencer(object):
    """Initialized with a sentencer and language parameter it stores the language related sentencer."""
    # this is a factory like part. It may go into different factory classes if needed
    # these are preprocessing regexps.
    rm_noise = re.compile('\s+')
    normal_punct = re.compile('\.+[?!]*|[?!:]') # XXX it might be useful for syntactic analysis

    def __init__( self, sentencer, language ):
        languages=['english']
        if language in languages:
            self.language = language
        else:
            raise ValueError('Language "',language,'" not implemented')

        # initialize the sentencer TODO: make it a hash switch
        try:
            if sentencer == 'punkt':  # here we load the picke learner.
                self.sentencer = nltk.data.load('tokenizers/punkt/'+language+'.pickle')
        except: 
            raise ValueError('Sentencer: "'+sentencer+'" not implemented')

        self.data = []

    def process( self, string ):
        """ Takes a string and returns a list of sentences. Non-comma punctuation is turned into . and whitespaces are removed. """
        e = Sentencer.normal_punct.sub(' .', string )
        e = Sentencer.rm_noise.sub( ' ',e )
        # make a factory here using self.sentencer
        return self.sentencer.tokenize(e)
