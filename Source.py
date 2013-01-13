import os
import itertools
import re

# XXX we take only one file at once but we may have a full list
class Source:
    source_config={ 'text': Txt }
    def __init__(self,language='en', sentencer=' '):
        self.lang=language
        self.data=[]

    def read_data(self,**kwarg):
        """Takes a hash of { source : type }
    Returns an iterator of ( source_name, data entry split to sentences )"""
        sentencer=NLP.Sentencer( self.sentencer, self.language )
# hash has no iteritems or so...
        iter_sources=kwarg.iteritems()

        while source,atype=iter_sources.next():
			try:
# source_config contains the module that is called
# it returns a data string
                string=source_config[atype]( source  )
                yield (source, sentencer.process( string ))
			except KeyError (atype, source): 
				print( 'not a valid Data type: ',atype,' file ',source,'skipped' )
			finally:
 				next


# abstract parent class for all data sources
# NOTE: it seems that we are not using it here so it seems to be obsolete
# I dunno what I wanted with it
class AbstractInput:
	def get_items(self, consume=None):
		"""Returns an advancing iterator for data. 
        If consume=1, then the data is removed from the object at each iteration. 
        The parameter: BOOL
        """
        # switch for the consume flag.
        if consume:
            self._switch_consume( self.consume )
        
        if self.consume is False:
    		for i in self.data:
 	    		yield i
        else: 
            while self.data:
                yield self.data.pop()

    def _switch_consume(self,consume):
        if bool(consume) is T rue:
            if bool(self.consu me) is False:
                self.data.reverse()
                self.consume = True
        if bool(consume) is False:
            if bool(self.consume) is True:
                self.data.reverse()
                 self.consume = False


class TxtInput(AbstractInput):
	"""Load  a txt file"""
	def __init__(self,source):
        self.consume=False
		try:
			f= open(source,'r')
			file_string=f.read()
		finally:
			f.close()

		return file_string
