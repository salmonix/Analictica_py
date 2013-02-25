import re
from math import log

# CAVEAT: the sentence head token is hard coded as id 0
class Elements(object):
    """Object containing obj.tokens and obj.texts. Optional argument: 
    datasource : iterator, that returns a 'tite', 'tokenlist' tuple"""

    def __init__(self, datasource=None):
        self.tokens = Tokens()
        self.sentences = Sentences()
        if datasource:
            for (title, tlist) in datasource:
                self.add_sentence_of_tokens(title, tlist)

    def add_sentence_of_tokens(self, title, tokenlist):
        """Convenience method to process a sentence into the text and token containers."""

        self.sentences.add_text(title)
        tokenlist.insert(0, '_head_')
        idx = self.tokens.add_tokenlist(tokenlist)

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
        self.S = 1.0  # helps to fix most calculations as floats

    # add_tokenlist
    def add_tokenlist(self, data):
        """ Takes a list of tokens and stores them the tokenlist instance. Returns the index number(s) for the token. """

        idxs = []
        for i in data:
            idxs.append(self.add_token(str(i)))
        return idxs

    def add_token(self, name, parent={}, children={}):
        self.S += 1
        if  name in self.names :  # token exists
            token = self.names[ name ]
            self.freq_add(token)
            # print ('exists: ' + name)
            return self.tokens[ token ].idx

        # new token hash is made here
        else:
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

class Links(Tokens):
    """Links are Tokens, only differ that their name is a tuple and we also have to store the source Tokens instance."""

    def __init__(self, source):
        self.active = []
        self.idx = 0
        self.no_of_tokens = 1
        self.tokens = []  # token id ->{token_obj}
        self.names = {}  # name -> id TODO: lookup using trie
        self.S = 1.0  # helps to fix most calculations as floats
        self.source = source

    def add_tokenlist(self, data):
        """ Takes a list of links and stores them the tokenlist instance. Returns the index number(s) for the token. """

        idxs = []
        for i in data:
            idx = (self.add_token((i[0], i[1])))
            self.tokens[idx].link_PMI(i[2])

        return idxs

    def links_PMI(self, link):
        return self.source[ link[0]].PMI(self.source[ link[1] ])



class Token(object):
    """Token object. The co_occurrence is a matter of definition."""
    __slots__ = ('co_occurrence', 'name', 'freq', 'idx', 'S', 'attribute')
    def __init__(self, name, idx, parent, freq=1.0):
        self.name = name
        self.idx = idx
        self.freq = freq
        self.co_occurrence = {}
        self.S = parent
        self.attribute = ()

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

    def PMI(self, B):
        """Pointwise Mutual Information PMI(A|B) = p(A&B) / p(A)xp(B)"""
        # print ('CO_OCC:' + str(self.co_occurrence))
        if B.idx in self.co_occurrence:
            return log(2, (self.co_occurrence[B.idx] * self.Space) / (self.freq * B.freq))
        else:
            return 0.0

class Link(Token):
    """Links are Tokens, only differ that their name is a tuple."""


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
        """Returns a title, text list iterator -> tuple for the given text titles. If nothing is passed returns for all."""

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
         #   print (sen)
            for c in range(1, len(sen)):  # skip the head token   # XXX no auto vivification
                token = tokens[ sen[c] ]
                for i in range(1, len(sen)):  # this is the all with all loop
                    if c != i:
                        if sen[i] in token.co_occurrence:
                            token.co_occurrence[ sen[i] ] += 1
                        else:
                            token.co_occurrence[ sen[i] ] = 1
        #            print (" %d : %d " % (c, i))
