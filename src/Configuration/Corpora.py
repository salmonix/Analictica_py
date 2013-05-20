# a link of Borg borg borg
import warnings
import os.path
from os import  getcwd
from Utils.File import check_path, get_path_iterator

class ConfigSource(object):

    # still can not manage composite source... :-(
    def __init__(self, corpus, **kwarg):
        for (k, v) in kwarg.iteritems():
            self.__dict__['sourcetype'] = k
            for (k2, v2) in v.iteritems():
                self.__dict__[k2] = v2
        self.runmode = None
        self.corpus = corpus

    @property
    def path(self):
        """ file like instances have path attribute. returns iterator of filenames """
        if not 'path' in self.__dict__:
            raise '"path" attribute is missing for this source'
            return

        return get_path_iterator(self.__dict__['path'])


# TODO: no_nlp is awkward. it is better to explicitly say what I want.
class ConfigSources(object):

    _sources = {'test' : {'Txt' : { 'path': os.path.join(os.getcwd(), 'Tests', 'Files', 'Analictica.test_text'),
                                    'filterwords' : os.path.join(os.getcwd(), 'Tests', 'Files', 'filterlists.yaml')
                                    },
                          },
                   'ATU_Motifchain' : {'ATU_Motifchain': {'path': '/home/salmonix/ATU_MASTER/ATU_Motifchain.txt',
                                                           'no_nlp' : True }},
                '10tales': {'Txt': { 'path': os.path.join(os.path.expanduser('~'), 'DARANYI_MOTYO', 'LEGUJABB', '10 tales') }}
                  }
    _shared_state = {}

    for k, v in _sources.iteritems():
        _shared_state[k] = ConfigSource(k, **v)

    def __init__(self):
        self.__dict__ = self._shared_state
        self.runmode = None


# a Borg.
class Config(object):

    _shared_state = { '_sources' : ConfigSources(),
                    }

    # configurator functions shall return a key -> object pair with the appropriate object stored in
    def __init__(self):
        self.__dict__ = self._shared_state
        self.runmode = 'CRITICAL'

    def sources(self, source=None):
        if source != None:
            return self._sources.__dict__[source]

        return self._sources

