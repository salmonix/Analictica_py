import re
import string

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
            tokeRex = re.compile(r"[\s%s]+" % string.punctuation)  # split on punctuation and whitespace. It means no abbreviations, for example
            self.tokenize = lambda s : tokeRex.split(s)
            return

        # try to load the non default tokenizers
        try:
            if tokenizer == 'PunktWord':  # this if-elif-else construct is very explicite but on intent
                try:
                    import nltk.data

                except:
                    print('% tokenizer can not be imported')
                self.tokenize = PunktWordTokenizer()
            else:
                raise ValueError(tokenizer + 'is not implemented.')

        except:
            raise ValueError(tokenizer + " tokenizer not implemented")


    def get_tokens(self, sequence):

        if self.stopwords:
            tokens = self.tokenize(sequence)
            from pprint import pprint
            print(' ------------------ ')
            pprint(tokens)
            return [ i for i in tokens if i not in self.stopwords ]  # we do not remove punct
        else:
            tokens = self.tokenize(sequence)
            return tokens


class Sentencer(object):
    """Initialized with a sentencer and language parameter it stores the language related sentencer.
    sentencer(str) -> list or str. default: x -> x"""
    # this is a factory like part. It may go into different factory classes if needed
    # these are preprocessing regexps.
    rm_noise = re.compile('\s+')
    normal_punct = re.compile('\.+[?!]*|[?!:]')  # XXX it might be useful for syntactic analysis

    def __init__(self, sentencer, language):

        if not sentencer:
            self._sentencer = lambda x : [ x ]
            return

        # try to load the non default sequencers
        # self._sentencer = lambda x : [ d for d in x.replace('\n', ' ') ] # reuse?
        languages = ['english']
        if language in languages:
            self.language = language
        else:
            raise ValueError('Language "', language, '" not implemented')

        try:
            if sentencer == 'punkt':  # here we load the picke learner.
                try:
                    from nltk.tokenize import sent_tokenize  # XXX: this is unlcear what it is doing exactly
                    self.sentencer = nltk.data.load('tokenizers/punkt/' + language + '.pickle')
                except:
                    print(sentencer + 'can not be imported ')
                    return None

        except:
            raise ValueError('Sentencer: "' + sentencer + '" has problems or not implemented')

        self.data = []

    def process(self, sequence):
        """ Takes a string and returns a list of sentences. Non-comma punctuation is turned into . and whitespaces are removed. """
        if self._sentencer:
            return self._sentencer(sequence)

