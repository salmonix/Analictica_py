from math import log
from Atoms import Atoms, Atom


# CAVEAT: the sentence head token is hard coded as id 0
class Elements(object):
    """Object containing obj.tokens and obj.texts. Optional argument: 
    datasource : iterator, that returns a 'tite', 'tokenlist' tuple"""

    def __init__(self, datasource=None):
        self.tokens = Atoms()
        self.sentences = Sentences(self.tokens)
        if datasource:
            for (title, tlist) in datasource:
                self.add_sentence_of_tokens(title, tlist)

    def add_sentence_of_tokens(self, title, tokenlist):
        """Convenience method to process a sentence into the text and token containers."""

        self.sentences.add_text(title)
        tokenlist.insert(0, '_head_')
        tokens = self.tokens.add_tokenlist(tokenlist)

        self.sentences.add_token_ids([ t.idx for t in tokens])



class Sentences(object):
    """Text container: stores the text transformed into sequences of token index numbers.
    CAVEAT: at the current state the distinction: title  - text ( sentences ) is not clear."""

    # TODO: in case of lots of texts it should be optimized
    def __init__(self, tokens):
        self.text = {}
        self.active = ''
        self.tokens = tokens

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

# these are copy-paste iterators but a. faster, b. I do not know the use cases
    def get_sentences_by_id(self):
        """Returns a list of token id's the sentence is built from."""
        for i in self.text.values():
            for s in i:
                yield s

    def get_sentences_by_object(self):
            """Returns a list of token id's the sentence is built from."""
            tokens = self.tokens.tokens
            for i in self.text.values():
                for s in i:
                    yield [ tokens[id] for id in s ]

    def get_sentences_by_name(self):
                """Returns a list of token id's the sentence is built from."""
                tokens = self.tokens.tokens
                for i in self.text.values():
                    for s in i:
                        yield [ tokens[id].name for id in s ]

    def add_co_occurrences(self, tokens):
        """Adds the co-occurrence of two words. The co_occurrences attribute is the data for joined computations.
        Possibly other occurrences can be calculated here, like syntagmatic co-occurrences."""

        # bug? : in case : 'a a' co_occurrence is : 2, not 1 !!!!!
        sentences = self.get_sentences_by_id()
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
