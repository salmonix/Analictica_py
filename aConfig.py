class Config(object):

    def __init__(self):
        self.sources = {'test' : ('Txt' , { 'path':'/home/salmonix/memdrive/Analictica.test_text' }),
                       'atu' : ('ATU', {'path': '/home/salmonix/DARANYI_MOTYO/ATU/ATU_files/' }),
                      }

        self.runmode = None

    def set_runmode(self, mode='debug'):
        self.runmode = mode
