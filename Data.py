import os
import itertools
import re

# XXX we take only one file at once but we may have a full list
class Source:
	"""Source factory - returning the proper data source instance

	Usage: Source( preparator='preparator','source1'='type1','source2'='type2', etc.)

	type: text, offer_description etc.
	source: a filename, connection parameter, etc.
	preparator: preparator is a - most probably - commander class 
	to process the input line. By default it is SourcePreparator.
	"""
	# this is a configuration here, Config Singleton candidate
	source_config={ #'offer_description' : Idealo_csv,
			'text': Txt }

	def __init__(self,lang='en'):
		self.lang=lang
		self.data=[]

	def get(preparator=None, **kwarg):
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
	def get_items(self):
		"""Returns an advancing iterator for data"""
		for i in self.data:
			yield i

	def get_items_reverse(self):
		"""Returns a backwarding iterator for data"""
		for i in range( len(self.data) ):
			yield self.data[i]

	def get_atoms(self,string):
# we should make it better. Now, 
# 0. colon: ok.
# 0a. - text - : ok.
# 1. punc+\s*+CAP = ok.
# 2. abbrev. + punc + [ normal: non boundary, CAP: boundary ]
###  sub elements
# it may go into an interative pattern : call it with a pattern and get an array
    

class TxtInput(AbstractSource):
	"""Load a txt file"""
	def __init__(self,source):
		try:
			f=open(source,'r')
			file_string=f.read()
		finally:
			f.close()

		self.data=self.get_atoms(file_string)
		return self
