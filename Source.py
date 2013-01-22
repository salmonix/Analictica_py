import os
import re

# XXX we take only one file at once but we may have a full list
class Readin(object):
    """Returns a generator which returns a data entry as title - data string.
    The connection parameters are stored in the following dictionary structure:
        sourcename : ( 'type', { parameter1 : value })
        where type is the name of the module that reads the data,
        the following dictionary stores the rest of the connection parameters, which is 
        path in the case of a file."""

    connections = {'test' : ( 'Txt' ,{ 'path':'/home/salmonix/memdrive/Analictica.test_text' } ) } # we should load it from file later
    @classmethod
    def list_connections(cls):
        return Readin.connections.keys()

    @staticmethod
    def _reader_factory( params ):
        con_type=params[0]
        con_params=params[1]
        if con_type == "Txt": return Txt(con_params).read_in()
        assert 0, "Bad shape creation: " + type

    def __init__(self):
        self.data=[]

    def read_data(self, *sources):
        """Takes source_name, returns an iterator of ( source_name, data string )
        It passes the wole dictionary entry of the tuple related to the sourcename(s)"""


        for sourcename in sources:
            try:
                # source_config contains the module that is called
                # it returns a data string split into sentences
                data_obj=Readin._reader_factory( Readin.connections[sourcename] )
                for i in data_obj: # we expect iterable returns. Each i is a string unit TODO: Test here !
                    yield ( sourcename, [i] ) 
            except KeyError (sourcename):
                print('Source '+sourcename+' is not defined.')
            finally:
                next

class Txt(object):
    """Load  a txt file"""
    def __init__(self,source):
        self.source = source['path'] # place for further checks etc.

    def read_in(self):
        with open(self.source,'r') as f:
            file_string = f.read()
        f.close()
        return [ file_string ]
