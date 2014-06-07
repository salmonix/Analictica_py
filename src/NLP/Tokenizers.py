import re
import string
import nltk.data
# from nltk.tokenize.punkt import PunktWordTokenizer
from nltk.tokenize import sent_tokenize  # this is the regexp based tokenizer

"""We should consider two more cases:
1. a method to handle the stopwords
2. a possibility of getting pos tags parallel with the tokens.
 The use of the second case is not really clear. Perhaps we should add metadata to the token and
 store that way."""

class Tokenizer(object):
    def __init__(self, tokenizer, language, stopwords=None):
        """tokenizer(str) -> list of str. default: str.split()
        language(str)  -> additional parameter to the aboves. default: none. 
        Note: the default tokenizer is a stone-axe tokenizer, as blindly removing all the punctuations and 
        splitting on \s. This will naturally destroy abbreviations, for example."""

        self.stopwords = stopwords
        if not tokenizer:
            self.tokenize = lambda s : [ d for d in  s.translate(string.maketrans(" ", " "), string.punctuation).split() if d ]
            return
        # try to load the non default tokenizers
        try:
            if tokenizer == 'PunktWord':
                self.tokenize = PunktWordTokenizer()
        except:
            raise ValueError(tokenizer + " tokenizer not implemented")

    def get_tokens(self, sequence):
        if self.stopwords:
            tokens = self.tokenize(sequence)
            return [ string.strip(i, string.punctuation) for i in tokens if i not in self.stopwords ]
        else:
            return self.tokenize(string)



class Sentencer(object):
    """Initialized with a sentencer and language parameter it stores the language related sentencer.
    sentencer(str) -> list or str. default: x -> x"""
    # this is a factory like part. It may go into different factory classes if needed
    # these are preprocessing regexps.
    rm_noise = re.compile('\s+')
    normal_punct = re.compile('\.+[?!]*|[?!:]')  # XXX it might be useful for syntactic analysis

    def __init__(self, sentencer, language):

        if not sentencer:
            self._sentencer = lambda x : [ d for d in x.split('\n') if d ]
            return

        # try to load the non default sentencers
        languages = ['english']
        if language in languages:
            self.language = language
        else:
            raise ValueError('Language "', language, '" not implemented')

        # initialize the sentencer TODO: make it a hash switch
        try:
            if sentencer == 'punkt':  # here we load the picke learner.
                self.sentencer = nltk.data.load('tokenizers/punkt/' + language + '.pickle')

        except:
            raise ValueError('Sentencer: "' + sentencer + '" has problems or not implemented')

        self.data = []

    def process(self, string):
        if self._sentencer:
            return self._sentencer(string)
        """ Takes a string and returns a list of sentences. Non-comma punctuation is turned into . and whitespaces are removed. """
        e = Sentencer.normal_punct.sub(' .', string)
        e = Sentencer.rm_noise.sub(' ', e)
        # make a factory here using self.sentencer
        return self.sentencer.tokenize(e)
