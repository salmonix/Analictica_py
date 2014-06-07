import os

from yaml import load, dump

try: 
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader as Loader, Dumper as Dumper

from Configuration import get_configuration

_files_configuration = Configuration('iotypes')

def iter_files(search_path, pattern, pathsep=os.pathsep):
     """ Given a search path, yield all files matching the pattern."""
     
     if os.path.isfile(search_path):
         yield search_path
         
     for path in search_path.split(pathsep):
         for match in glob.glob(os.path.join(path, pattern)):
             yield match


def open_file(fpath,**kwargs):
    """Ambitiously tries to open any file returning a filehandler"""
    
    ext = fpath[ fpath.rfind('.')+1 : ] # get the extension
    mode = ''
    
    try:
        mode = kwargs['mode']
    except:
        mode='r'
        
    try:
        mod = None
        if ext in kwargs['extensions'][ext]:
            mod = kwargs['extensions'][ext]
        else:
            print('file extension %s is not recognized. trying "txt" ' % ext )
            mod = 'txt'

        # we make yaml a default format as it is need to load all the configuration data that is in yaml
        if mod not in ['yaml', 'yml']:

            if mod in _files_configuration.filetypes:
                # get opener
                opener = _files_configuration.filetypes[mod]

        with open(fpath,mode) as fh:       
            return fh
        
    except:
        raise IOError('Unable to open %s' %(fpath ) )
        return None

def check_path(fpath, *args):
     """Checks for the existence of a path. The arguments are joined into one path string."""

     if os.path.exists(fpath):
         return fpath
     else:
         # warnings.warn("Not existing: " + fpath)
         raise IOError("{} does not exist.".format(fpath))
         return None


class File(object):
    """The file wrapper returning file iterator with guessing the correct access to the given file.
    
    The guessing uses the file-type indicator in the following order:
    - passed in kwargs[extension]
    - using the file extension and matching it with the content of config/iotypes.yaml
    - falling back to simple txt type
    
    """
    __slots__=('fpath','fh','filelist','_pointer')
    
    def __init__(self,fpath,*args,**kwargs):
        """ constructor. the *args parameters are joined, the kwargs[extension] is used for custom idenfification of the file-type."""
        fpath = check_path(fpath,*args)

        if not path:
            return None

        if os.path.isdir(fpath):
            self.filelist = os.walk(fpath)
        else:
            self.filelist = [ fpath ]
        
        self.active_file = self._get_active_file()
        self.active_fh = open_file(self.active_file)

    def __iter__(self):

        try:
            line = self.active_fh.readline()

            if line:
                yield line
            else:
                while True:
                    try:
                        self.active_file = self._get_active_file()
                    except:
                        print('Filelist is exhausted.') # info loglevel
                        yield None
                
                    self.active_fh = open_file(self.active_file)
                    line = self.active_fh.readline()

                    if line:
                        yield line 
                
        except:
            raise IOError

    def _get_active_file(self):
        for f in self.filelist:
            yield f