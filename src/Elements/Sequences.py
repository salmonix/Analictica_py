from math import log
import Token

class Sequences(object):
    """Sequences are an other concept of the universe. These are the visible phenomenae, the product of 
    engines applying relations. The original input - for example text - is the starting sequence, but 
    any graph can be a sequence. These are not entities, but end-products or sources,
    a combination of different elements of rules and relations.
    Every sequence must know iteritems() in the base class.
    Init parameters: 
        - tokens instance
        Bool:
        - increment_co-occurrence (True) : automatically increment the co-occurrences as a sequence is given.
            Otherwise self.add_co_occurrences must be called.
        - drop_duplicates (True) : if a sequence appeares multiple times in a text unit, it is dropped
        - head_token (False) : the abstract head token is counted or not
    """

    def __init__(self, tokens, increment_co-occurrence=True, drop_duplicates=True, head_token=False):
        self._sequence = {}
        self.active = ''
        self.tokens = tokens
        self.increment_co-occurrence = increment_co-occurrence
        self.drop_duplicates = drop_duplicates
        self.head_token=head_token
        if head_token is True:
            tokens.insert(0, '_head_')


    def add_sequence_of_tokens(self,sequence):
        """Processes the sequence of tokens into the instance sequence container"""

        sequences.add_unit(title)
        sequences.add_token_ids([ t.idx for t in sequence])
        if self.increment_co-occurrence:
            add_co_occurrence(sequence)


    def add_co_occurrences(self,sequence=None):
        """Adds the co-occurrence of two words. The co_occurrences attribute is the data for joined computations.
        It is important that co-occurrence may mean different things. At the moment we think that two elements 
        appeare in the same sequence."""

        if not sequence:
            sequence = self.sequences.text.values()
        # bug? : in case : 'a a' co_occurrence is : 2, not 1 !!!!!
        for sequences in self.sequences.text.values():  # get the list of sentences

            for sen in sequences:  # iterate over the sentences
                self._add_co-occurrence(sen)
             #   print (sen)
       

    def _add_co-occurrence(self, sequence ):

        tokens = self.token.tokens # TODO: interface will change
        sequences = self.sequences

        for c in range(0, len(sequence)): # XXX check head token case
            token = tokens[ sen[c] ]
            for i in range(1, len(sequence)):  # this is the all with all loop
                if c != i:
                    if sen[i] in token.co_occurrence:
                        token.co_occurrence[ sequence[i] ] += 1
                    else:
                        token.co_occurrence[ sequence[i] ] = 1
            # print (" %d : %d " % (c, i))

    # TODO: sequences will get a list of sequences.
    def add_unit(self, source):
        """Start a new sequence unit."""
        
        if source in self.text and self.drop_duplicates is True:
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


    @property
    def sequence(self):
        if self._sequence == 'pkl':
            """ read in pkl. we should also set a handler to save it after a while..."""
        
        return self._sequence[active]

