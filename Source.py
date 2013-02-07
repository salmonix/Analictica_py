import os
import re
import copy
from aConfig import Config

class Corpus(object):
    """Returns a generator which returns a data entry as title - data string.
    The connection parameters are stored in the following dictionary structure:
        sourcename : ( 'type', { parameter1 : value })
        where type is the name of the module that reads the data,
        the following dictionary stores the rest of the connection parameters, which is 
        path in the case of a file."""

    connections = Config().sources
    @classmethod
    def list_connections(cls):
        return Corpus.connections.keys()

    @staticmethod
    def _reader_factory(con_type, con_params):
        if con_type == "Txt": return Txt(con_params).read_in()
        if con_type == "ATU": return ATU(con_params).read_in()
        raise ValueError(con_type + ' is not recognized type')

    def process(self, source):
        """Processes a source and returns an Elements instance of the processed data. Source names are case insensitive."""
        title = source.lower()
        source = Corpus.connections[title]
        path = source[1]['path']

        if os.path.isfile(path):
            source_iterator = self._read_data(source[0], source[1])
            for data in source_iterator:
                for i in data:
                    yield title, i

        elif os.path.isdir(path):
            source = copy.copy(source)
            for f in os.listdir(path):
                print (f)
                source[1]['path'] = os.path.join(path, f)
                title = os.path.basename(f)
                for data in self._read_data(source[0], source[1]):
                    for i in data:
                        yield title, i

    def _read_data(self, con_type, con_params):
        """Takes source_name and connection parameters, returns an iterator of ( source_name, data string )
        It passes the wole dictionary entry of the tuple related to the sourcename(s)"""
        # source_config contains the module that is called
        # it returns a data string split into sentences
        data_obj = Corpus._reader_factory(con_type, con_params)
        for i in data_obj:  # we expect iterable returns. Each i is a string unit TODO: Test here !
            yield [i]

class Txt(object):
    """Load a txt file. The class requires 'path' parameter. """
    def __init__(self, source):
        self.source = source['path']  # place for further checks etc.

    def read_in(self):
        with open(self.source, 'r') as f:
            file_string = f.read()
        f.close()
        return [ file_string ]

# clear it up, check regexp etc.
class ATU(Txt):
    """Reads an ATU, which is a type of text file. Requires 'path' parameter."""
    # closures_cfs = re.compile('\[.*?\]|cf\..*?\.')
    def __init__(self, source):
        super(ATU, self).__init__(source)  # python3: super().__init__( source )

    def read_in(self):
        data = super(ATU, self).read_in()
        # data = closures_cfs.sub('', data)
        return data
