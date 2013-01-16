# abstract parent class for all data sources
# NOTE: it seems that we are not using it here so it seems to be obsolete
# I dunno what I wanted with it
class AbstractInput:
    def get_items(self, consume=None):
        """Returns an advancing iterator for data. 
        If consume=1, then the data is removed from the object at each iteration. The parameter: BOOL"""
        
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


