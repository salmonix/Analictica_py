import os
import itertools
import re

# XXX we take only one file at once but we may have a full list
class Source:
	"""Sou rce factory - returning the proper data source instance

	Usage: Source( sentencer, language)

    sentencer: defaults to nltk.tokenize.punkt.
    language: defaults to 'en'.

    The return object contains a list of lists of splitted sentences.
	"""
	# this is a configuration here, Config Singleton candidate
	source_config={ #'offer_description' : Idealo_csv,
			'text': Txt }

	def __init__(self,language='en', sentencer=' '):
		self.lang=language
 		self.data=[]

	def read(**kwarg):
    """	read( source1='type1', source2='type2'...)

    Fills the object with the passed sources.
    type: text, offer_description etc.
	source: a filename, connection parameter, etc.
    
    """

		# here we loop over the dict and aggregate the sources that are returned
		iter_sources=kwarg.iteritems()
		while source,atype=iter_sources.next():
			try:
 				source_obj=source_config[atype]( source,preparator  )
				data.append( source.obj.data )
			except KeyError (atype, source): 
				print( 'not a valid Data type: ',atype,' file ',source,'skipped' )
			finally:
 				next


# abstract parent class for all data sources
class AbstractInput:
	def get_items(self, consume=None):
		"""Returns an advancing iterator for data. 
        If consume=1, then the data is removed from the object at each iteration. 
        Note: in this case the object data order and integrity may not be maintained,
        so use it with care. The parameters: BOOL
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
        if bool(consume) is True:
            if bool(self.consume) is False:
                self.data.reverse()
                self.consume = True
        if bool(consume) is False:
            if bool(self.consume) is True:
                self.data.reverse()
                 self.consume = False


class TxtInput(AbstractInput):
	"""Load a txt file"""
	def __init__(self,source):
        self.consume=False
		try:
			f=open(source,'r')
			file_string=f.read()
		finally:
			f.close()

		return self
