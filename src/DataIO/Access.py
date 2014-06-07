import os
import re
import copy
from Configuration import Configuration # clean up namespace

class Formatter(object):
    """Abstract Class for accessing the formats. Each element of the class returns an iterator
    that yields a 'title' and a [ string ] at each call."""


    class Txt:
        """Load a txt file. The class requires 'path' parameter. """
        def __init__(self, path):
            self.path = path  # place for further checks etc.
    
        def read_in(self):
            with open(self.path, 'r') as f:
                file_string = f.read()
    
            title = os.path.basename(self.path)
            yield title, [ file_string ]
    
    
    class ATU_Motifchain:
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

    class YAML:
        pass


class Access(object):
    """A not so Abstract Class for accessing the data source"""

    def __init__(self,corpus='test'):
        config = Configuration('Source',corpus)
        for source_module in 'File','Database':
            
            if hasattr(config, cource):
                pass
