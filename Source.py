import os
import re

# XXX we take only one file at once but we may have a full list
class Readin(object):
    """Returns a generator which returns a data entry as title - data string."""

    connections = {'test' : ( 'Txt' ,{ 'address':'/home/salmonix/memdrive/Analictica.test_text' } ) } # we should load it from file later
    @classmethod
    def list_connections(cls):
        return Readin.connections.keys()

    @staticmethod
    def _reader_factory( params ):
        con_type=params[0]
        con_params=params[1]
        if con_type == "Txt": return Txt(con_params)
        assert 0, "Bad shape creation: " + type

    def __init__(self):
        self.data=[]

    def read_data(self, *sources):
        """Takes source_name, returns an iterator of ( source_name, data string )"""

        for sourcename in sources:
            try:
                # source_config contains the module that is called
                # it returns a data string split into sentences
                data_obj=Readin._reader_factory( Readin.connections[sourcename] )
                for i in data_obj: # we expect iterable returns
                    yield ( i, source ) 
            except KeyError (sourcename):
                print('Source '+sourcename+' is not defined.')
            finally:
                next

class Txt(object):
    """Load  a txt file"""
    def __init__(self,source):
        self.consume = False
        try:
            f = open(source,'r')
            file_string = f.read()
        finally:
            f.close()
            
        return [ file_string ]
