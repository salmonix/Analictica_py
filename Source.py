import os
import re
import copy

from Configuration import Corpora

from NLP.Tokenizers import Tokenizer, Sentencer
from NLP.Filters import Stopword

class Corpus(object):
    """Returns a generator which returns a data entry as title - data string.
    The connection parameters are stored in the following dictionary structure:
        sourcename : ( 'type', { parameter1 : value })
        where type is the name of the module that reads the data,
        the following dictionary stores the rest of the connection parameters, which is 
        path in the case of a file."""

    @staticmethod
    def _reader_factory(con_type, con_params):
        # should be more clever
        if con_type == "Txt": return Txt(con_params)
        if con_type == "ATU_Motifchain": return ATU_Motifchain(con_params)
        raise ValueError(con_type + ' is not recognized type')

    def __init__(self, source):
        self.title = source.lower()
        self.source = Corpora().sources(source)

    def tokenize_source(self, sentencer=None,  # that is equal to none.
                              tokenizer=None,
                              language=None):
        """Returns an iterator of ( 'title', tokens[] ). Optional parameters are:
        sentencer(str) -> list or str. default: x -> x
        tokenizer(str) -> list of str. default: str.split()
        language(str)  -> additional parameter to the aboves. default: none. """

        self.sentencer = Sentencer(sentencer, language)
        self.tokenizer = Tokenizer(tokenizer, language)

        for (title, text) in self.read_data():
            if hasattr(self.source, 'no_nlp'):  # XXX we stop here for some reason
                # print(text)
                yield title, text
            else:
                for s in self.sentencer.process(text):
                    tokens = self.tokenizer.get_tokens(s)
                    yield title, tokens


    def read_data(self):
        """Returns an iterator of ( 'title', 'line' )"""

        for spath in self.source.path:  # iterate the source paths ( can be multiple )
            Source_obj = Corpus._reader_factory(self.source.sourcetype, spath)  # it returns the proper read_in iterator for the source
            for title, text in Source_obj.read_in():  # read in reads the whole file
                for i in text:
                    yield title, i


class Txt(object):
    """Load a txt file. The class requires 'path' parameter. """
    def __init__(self, path):
        self.path = path  # place for further checks etc.

    def read_in(self):
        with open(self.path, 'r') as f:
            file_string = f.read()

        title = os.path.basename(self.path)
        yield title, [ file_string ]

# XXX perhaps it should be vice versa - these would be the decorators of the Txt object
class ATU_Motifchain(Txt):
    """Reads an ATU, which is a type of tabbed text file, a head and tail type..."""

    head_n_tail = re.compile(r'.*\t.*')

    def __init__(self, source):
        super(ATU_Motifchain, self).__init__(source)  # python3: super().__init__( source )

    def read_in(self):
        with open(self.path, 'r') as f:

            for row in f.readlines():
                row = row.split('\t')
                row[-1] = row[-1].strip('\n')
                yield row[0], [ row[1:] ]

