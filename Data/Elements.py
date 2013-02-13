import re
from math import log
from copy import copy

from NLP.Tokenizers import Tokenizer, Sentencer
from NLP.Filters import Stopword

from Modules.Abacus import entropy, probability


# CAVEAT: the sentence head token is hard coded as id 0
class Elements(object):
    """Object containing obj.tokens and obj.texts with some additional convenience methods on the top."""

    def __init__(self, sentencer, tokenizer, language):
        self.sentencer = Sentencer(sentencer, language)
        self.tokenizer = Tokenizer(tokenizer, language)

        self.tokens = Tokens()
        self.sentences = Sentences()

    def process_datastring(self, title, data):
        sentences = self.sentencer.process(data)
        for s in sentences:
            tokens = self.tokenizer.get_tokens(s)
            self.add_data(title, tokens)

    def add_data(self, source, tokenlist):
        """Convenience method to process a sentence into the text and token containers."""
        self.sentences.add_text(source)
        tokenlist.insert(0, '_head_')
        idx = self.tokens.add_token(tokenlist)

        self.sentences.add_token_ids(idx)


class Tokens(Elements):
    """Container for the tokens, the nodes. Token container is not optimal for deletion."""

    def __init__(self):
        """The initial token is _head , which is the head of a sequence."""

        self.active = []
        self.idx = 0
        self.no_of_tokens = 1
        self.tokens = []  # token id ->{token_obj}
        self.names = {}  # name -> id TODO: lookup using trie
        self.S = 1.0  # helps to fix most calculations as

    def add_token(self, data):
        """ Takes a string or list of strings ( tokens ) and stores in the tokenlist. Returns the index number(s) for the token. """

        if isinstance(data, str):  # add a string - obsolete
            return self._add_token(data)
        elif isinstance(data, list):  # add a list of strings
            idxs = []
            for i in data:
                idxs.append(self._add_token(i))
            return idxs

    def _add_token(self, name, parent={}, children={}):
        if  name in self.names :  # token exists
            token = self.names[ name ]
            self.freq_add(token)
            # print ('exists: ' + name)
            return self.tokens[ token ].idx

        # new token hash is made here
        else:
            self.S += 1
            self.tokens.append(Token(name, self.idx, self))
            self.names[name] = self.idx
            # print ('no exists : ' + name)
            idx = self.idx
            self.idx += 1
            return idx

    def get_token(self, token):
        """Gets a token_id  ( index ) -> returns a token """

        return self.idx(token_id)

    def freq_add(self, token, num=1):
        if type(token) is str:
            token = self.names[token]  # get the id

        self.tokens[token].freq_add(num)
        return self.tokens[token].freq


class Token(object):
    """Token object. The co_occurrence is a matter of definition."""
    __slots__ = ('co_occurrence', 'name', 'freq', 'idx', 'S', 'attribute', 'aux')
    def __init__(self, name, idx, parent, freq=1.0):
        self.name = name
        self.idx = idx
        self.freq = freq
        self.co_occurrence = {}
        self.S = parent
        self.attribute = {}
        self.aux = None

    def freq_add(self, num=1):
        self.freq += num

    @property
    def Space(self):
        """The probability space."""
        return self.S.S

    @property
    def shannon(self):
        """Shannon entropy for the token: -p(A)*log2( p(A) ) 
        If frequency is not set it returns 1.0."""

        if self.freq != 0:
            try:
                # print ('FREQUENCY: ' + str(self.freq) + ' SPACE: ' + str(self.Space))
                p = self.freq / self.Space
                # print ('Probability: ' + str(p))
                # print ('Shannon: ' + str(-1 * p * log(p, 2)))
                return -1 * p * log(p, 2)
            except:
                raise ValueError('calculation went wrong')
        else:
            return 1.0

    @property
    def probability(self):
        """Standard probability: freq/Space"""

        return self.freq / self.Space

    def conditional_probability(self, B):
        """Conditional probability on B: p(A&B)/P(B)"""
        if B.idx in self.co_occurrence:
            return self.freq / self.Space * self[ B.co_occurrence[ B.idx ] ]
        else:
            return 0.0

    # well, it is not optimized because of a number of zero lookup
    # but well fits the design.
    def PMI(self, B):
        """Pointwise Mutual Information PMI(A|B) = p(A&B) / p(A)xp(B)"""
        # print ('CO_OCC:' + str(self.co_occurrence))
        if B.idx in self.co_occurrence:
            return -1 * log(2, (self.co_occurrence[B.idx] * self.Space) / (self.freq * B.freq))
        else:
            return 0.0

class Sentences(object):
    """Text container: stores the text transformed into sequences of token index numbers."""

    # TODO: in case of lots of texts it should be optimized
    def __init__(self):
        self.text = {}
        self.active = ''

    def add_text(self, source):
        """Start a new text unit."""

        if source in self.text:
            return self.text[source]

        self.text[source] = []
        self.active = source

    def add_token_ids(self, idxs):
        self.text[ self.active ].append(idxs)

    def get_text(self, title=[]):
        """Returns a title, text list tuple for the given text titles. If nothing is passed returns for all."""

        # XXX name changed : get_text
        if title == []:
            title = self.text.keys()
            for t in title:  # this is each sentence list
                yield (t, self.text[t])

    def get_sentences(self):
        for i in self.text.values():
            for s in i:
                yield s

    def add_co_occurrences(self, tokens):
        """Adds the co-occurrence of two words. The co_occurrences attribute is the data for joined computations.
        Possibly other occurrences can be calculated here, like syntagmatic co-occurrences."""

        # bug? : in case : 'a a' co_occurrence is : 2, not 1 !!!!!
        sentences = self.get_sentences()
        tokens = tokens.tokens
        for sen in sentences:
            # print (sen)
            for c in range(1, len(sen)):  # skip the head token   # XXX no auto vivification
                token = tokens[ sen[c] ]
                for i in range(1, len(sen)):  # this is the all with all loop
                    if c != i:
                        if sen[i] in token.co_occurrence:
                            token.co_occurrence[ sen[i] ] += 1
                        else:
                            token.co_occurrence[ sen[i] ] = 1
                    # print (" %d : %d " % (c, i))
