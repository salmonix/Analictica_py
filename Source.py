import os
import re
import NLP.Sentencer

# XXX we take only one file at once but we may have a full list
class Source(object):

    source_config={ 'text': 'TxtInput' }

    def __init__(self,language='en'):
        self.lang=language
        self.data=[]

    def read_data(self,**kwarg):
        """Takes a hash of { source : type }
        Returns an iterator of ( source_name, data entry split to sentences )"""
        if self.sentencer == 'default':
            sentencer=NLP.Sentencer( self.sentencer, self.language )

        iter_sources=kwarg.iteritems()

        for source,atype in iter_sources():
            atype = atype.lower()
            try:
                # source_config contains the module that is called
                # it returns a data string split into sentences
                string=source_config[atype]( source  )
                yield (source, sentencer.process( string ))  # error : TxtInput is not yielding
            except KeyError (atype, source):
                print( 'not a valid Data type: ',atype,' file ',source,'skipped' )
            finally:
                next


class TxtInput(object):
    """Load  a txt file"""
    def __init__(self,source):
        self.consume = False
        try:
            f = open(source,'r')
            file_string = f.read()
        finally:
            f.close()
            
        return file_string

# AbstractInput was an iterator for the case of having iterable objects ( eg. database, csv ) where 
# each line is a source. TxTInput should yield a (whole) document at once, too.
