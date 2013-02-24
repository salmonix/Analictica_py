# a link of Borg borg borg
# __init__ is copy-paste !

# a Borg

import os.path

class ConfigSource(object):

    # still can not manage composite source... :-(
    def __init__(self, **kwarg):
        for (k, v) in kwarg.iteritems():
            self.__dict__['sourcetype'] = k
            for (k2, v2) in v.iteritems():
                self.__dict__[k2] = v2
        self.runmode = None

    @property
    def path(self):
        path = self.__dict__['path']

        if os.path.isdir(path):
            try:
                for f in os.listdir(path):
                    print (f)
                    fpath = os.path.join(path, f)
                    base = os.path.basename(f)
                    yield base, fpath
            except:
                print(' We have some error... ?')
        else:
            yield os.path.basename(path), path


class ConfigSources(object):

    _sources = {'test' : {'Txt' : { 'path':'/home/salmonix/memdrive/Analictica.test_text' }},
                   'atu' : {'ATU': {'path': '/home/salmonix/DARANYI_MOTYO/ATU/ATU_files/' }},
                  }
    _shared_state = {}

    for k, v in _sources.iteritems():
        _shared_state[k] = ConfigSource(**v)

    def __init__(self):
        self.__dict__ = self._shared_state
        self.runmode = None


# a Borg.
class Config(object):

    _shared_state = { '_sources' : ConfigSources() }

    # configurator functions shall return a key -> object pair with the appropriate object stored in
    def __init__(self):
        self.__dict__ = self._shared_state
        self.runmode = None

    def sources(self, source=None):
        if source != None:
            return self._sources.__dict__[source]

        return self._sources


a = Config().sources()
print(a.__dict__)
