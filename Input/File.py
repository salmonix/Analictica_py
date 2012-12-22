import io


class InputData:
	"""Returns an input object, with three methods:
	->read_entry() : returns an entry 
	->read_title() : returns the title for the entry
	->read_all()   : returns a concatenated string of title+entry"""
	def __init__(self,request):
		# get the connection configuration data
		path='./Import/config.xml'
		file=open(path,'w')
