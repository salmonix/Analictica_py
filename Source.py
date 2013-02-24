import os
import re
import copy

from aConfig import Config

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
        if con_type == "Txt": return Txt(con_params)
        if con_type == "ATU": return ATU(con_params)
        raise ValueError(con_type + ' is not recognized type')

    def __init__(self, source):
        self.title = source.lower()
        self.source = Config().sources(source)

    # this can be a decorator ( but I doubt we'll need that. This is a logical step closing a read_in process )
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

# clear it up, check regexp etc. -> this should be a tokenizer!
class ATU(Txt):
    """Reads an ATU, which is a type of text file. Requires 'path' parameter."""
    # closures_cfs = re.compile('\[.*?\]|cf\..*?\.')
    def __init__(self, source):
        super(ATU, self).__init__(source)  # python3: super().__init__( source )

    def read_in(self):
        txt_iterator = super(ATU, self).read_in()
        # data = closures_cfs.sub('', data)
        return txt_iterator
