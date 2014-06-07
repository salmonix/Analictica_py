import os

from yaml import load, dump
try: 
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader as Loader, Dumper as Dumper


CONFIGPATH='config/'

# module globals for caching
_configuration = {}

def get_configuration(config_name,for_key='For',force_reload=False): # force reload may not be necessary
    """Reads the configuration 'yaml' file and returns an instance of Configuration on success,
    raises exceptions and returns None otherwise.
    config_name: the name of the config file w/o the '.yaml' suffix
    for_key: if a config file contains multiple top-entries, this key chooses one."""

        cache_key = '||'.join([config_name, for_key])
                 
        if cache_key in _configuration and not force_reload: 
            return _configuration[cache_key]

        config = _get_configfile('.'.join([config_name,'yaml']))
        if not config:
            return None

        if for_key:
            try:
                config = config[for_key]
            except KeyError:
                print('Missing entry {} in file  {} '.format(for_key, _configuration_paths[configure] ) )
            finally:
                return None

        # do caching
        config = Configuration(_configuration )
        _configuration[cache_key] = config
        return config

# to get the initial state of the config data and circular dependencies this is a slim module. Perhaps an initial bootstrapping method would be more savvy
def _get_configfile(fpath):
    
    try:
        fh = open(fpath,'r')
        data = load(fh, Loader=Loader )
        
    except IOError as err:
        print('Unable to open {} , {}'.format(fpath,err ) )
    except Exception as err:
        raise('Unknown exception: '.format(err))


class Configuration(object):
    
    def __init__(self,_configuration):
        self = _configuration
        self.__dict__ = _configuration.keys()