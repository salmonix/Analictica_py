from math import log
from Atoms import Atoms, Atom


# can it be a  Builder class?

def add_sequence_of_tokens(sequences, title, tokenlist):
        """Convenience method to process a sequence into the text and token containers."""

        sequences.add_text(title)
        tokenlist.insert(0, '_head_')
        tokens = self.tokens.add_tokenlist(tokenlist)

        sequences.add_token_ids([ t.idx for t in tokens])

def add_co_occurrences(sequences, tokens):
        """Adds the co-occurrence of two words. The co_occurrences attribute is the data for joined computations.
        It is important that co-occurrence may mean different things. At the moment we think that two elements 
        appeare in the same sequence."""

        tokens = token.tokens

        # bug? : in case : 'a a' co_occurrence is : 2, not 1 !!!!!
        for sequences in sequences.text.values():  # get the list of sentences

            for sen in sequences:  # iterate over the sentences
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



class Sequences(object):
    """Sequences are an other concept of the universe of communication. These are the visible phenomenae, the product of 
    engines applying relations. The original input - for example text - is the starting sequence, but 
    any graph can be a sequence. These are not entities, but end-products, a combination of different elements 
    of rules and relations.
    Every sequence must know iteritems() in the base class."""

    def __init__(self, tokens):
        self.sequence = {}
        self.active = ''
        self.tokens = tokens

    def add_text(self, source):
        """Start a new text unit."""

        if source in self.text:
            return self.text[source]

        self.sequence[source] = []
        self.active = source

    def add_token_ids(self, idxs):
        self.text[ self.active ].append(idxs)

    def get_sequence(self, title=[]):
        """Returns a title, text list iterator -> tuple for the given text titles. If nothing is passed returns for all."""

        # XXX name changed : get_text
        if title == []:
            title = self.sequence.keys()
            for t in title:  # this is each sentence list
                yield (t, self.sequence[t])

# these are copy-paste iterators but a. faster, b. I do not know the use cases
    def get_senquences_by_id(self):
        """Returns a list of token id's the sentence is built from."""
        for title, i in self.sequence.iteritems():
            for s in i:
                yield title, s

    def get_sequences_by_object(self):
            """Returns a list of token id's the sentence is built from."""
            tokens = self.tokens.tokens
            for title, i in self.sequence.iteritems():
                for s in i:
                    yield title, [ tokens[id] for id in s ]

    def get_sequences_by_name(self):
                """Returns a list of token id's the sentence is built from."""
                tokens = self.tokens.tokens
                for title, i in self.sequence.iteritems():
                    for s in i:
                        yield title, [ tokens[id].name for id in s ]
