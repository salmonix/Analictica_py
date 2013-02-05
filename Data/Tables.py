from numpy import zeros, dtype
from functools import partial
import sys

class Table(object):
    def __init__(self, tokens):
        self.tokens = tokens.tokens
        dim = tokens.S - 1  # space starts from 1, lists from 0
        self.array = zeros((dim, dim), dtype=float)  # the given tablespace is always overwritten

    # simple tables
    def build_table(self, method):
        """Simple tables : takes an attribute of key:value type, where
        key: tokenid, value: value in relation to the referring token;
        builds a table as token X token with the referring value in the cell.
        If the method is callable, then it supposedly is some kind of joined method ( eg. joined probability )
        and the attribute co_occurrence is used assuming that it contains the relevant data - eg. co_occurrence with other
        tokens, in a dictionary. So, it is used instead of iterating over token x token times and letting each token
        run this check internally."""

        for xToken in self.tokens:
            yTokens = ''
            try:
                # print(attribute)
                # print (xToken)
                yMethod = getattr(xToken, method)
                # print (yTokens)
            except:
                raise ValueError

            x = xToken.idx

            if hasattr(yMethod, '__iter__'):  # iterable
                # print ('yMethod: ' + str(yMethod))
                try:
                    for y, v in yMethod.items():
                        # print ("x: %2d y: %2d -> %3d" % (x, y, v))
                        self.array[x][y] = v
                except:
                    next

            elif hasattr(yMethod, '__call__'):  # callable
                try:
                    fun = partial(yMethod)  # Currying XXX: does it improve speed?
                except:
                    raise ValueError('Unable to get partial function from method ' + str(method))

                # print ('Indexes: ' + str(x) + ' : ' + str(xToken.co_occurrence))
                try:
                    for yTokenId in xToken.co_occurrence.keys():
                        y = self.tokens[yTokenId].idx
                        self.array[x][y] = fun(self.tokens[yTokenId])
                except:
                    print ('Exception')
                    next

            else:
                raise ValueError('Parameter method returns neither iterable nor function.')

        return self.array


    def write_formatted(self, writer ):  # takes also : target object
        # if there is not table -> formatting must fail instead of creating an empty table
        # it will not work with ARRAYs  - we must write it immediately out to the passed object
        header = [ t.name for t in self.tokens]
        writer.append(header)
        for i in range(0, len(header)):
            row = []
            row.append(header[i])
            for e in self.array[i]:
                row.append(e)
            writer.append(row)
            # target.write(header[i], self.array[i])

        # writer.close()
        return 1 # deal with the error cases

class WriteTable(object):
    
    def __init__(self, format='csv', target='stdout'):
        # writers
        if target == 'stdout':
            self.writer = sys.write(target) # we write to the file or whatever, but we must open!!
        # formatters
        if format == 'csv':
            self.formatter( BuildCSV(separator = ',') )  # may require a separator
        
    def append(self,row):
        self.data.append(row)
        
    def close(self): # a dummy for printing the screen
        pass
        
class WriteScreen(WriteTable):
    def append(self,row):
        