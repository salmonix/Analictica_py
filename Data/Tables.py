from numpy import zeros, dtype
from functools import partial
import sys

class Table(object):
    def __init__(self, tokens):
        self.tokens = tokens


    # simple tables
    def build_table(self, method):
        """Simple tables : takes an attribute of key:value type, where
        key: tokenid, value: value in relation to the referring token;
        builds a table as token X token with the referring value in the cell.
        If the method is callable, then it supposedly is some kind of joined method ( eg. joined probability )
        and the attribute co_occurrence is used assuming that it contains the relevant data - eg. co_occurrence with other
        tokens, in a dictionary. So, it is used instead of iterating over token x token times and letting each token
        run this check internally."""
        dim = self.tokens.idx - 1  # space starts from 1, lists from 0
        table = zeros((dim, dim), dtype=float)  # the given tablespace is always overwritten

        for xToken in self.tokens.tokens:
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
                        table[x][y] = v
                except:
                    next

            elif hasattr(yMethod, '__call__'):  # callable
                try:
                    fun = partial(yMethod)  # not faster but clearer
                except:
                    raise ValueError('Unable to get partial function from method ' + str(method))

                # print ('Indexes: ' + str(x) + ' : ' + str(xToken.co_occurrence))
                try:
                    for yTokenId in xToken.co_occurrence.keys():
                        y = self.tokens.tokens[yTokenId].idx
                        table[x][y] = fun(self.tokens.tokens[yTokenId])
                except:
                    assert'Exception'
                    next

            else:
                raise ValueError('Parameter method returns neither iterable nor function.')

        self.table = table
        return table

# ## TODO
# ehh, a = numpy.asarray([ [1,2,3], [4,5,6], [7,8,9] ])
# numpy.savetxt("foo.csv", a, delimiter=",")

    def write_formatted(self, **kwargs):  # takes also : target object
        # if there is not table -> formatting must fail instead of creating an empty table
        # it will not work with ARRAYs  - we must write it immediately out to the passed object

        writer = WriteTable(**kwargs)
        header = [ t.name for t in self.tokens.tokens]
        writer.write(header)
        for i in range(1, len(header)):
            row = []
            row.append(header[i])
            for e in self.table[i - 1]:
                row.append(e)
            writer.write(row)

        writer.close()
        return 1  # deal with the error cases

# should go into an Exporters namespace
class WriteTable(object):

    def __init__(self, format='csv', target=None, file=None):
        # writers
        if target == 'stdout':
            self.target = sys.stdout
        elif file:
            try:
                self.target = open(file, 'w')
            except:
                self.target.close()
                raise IOError

        else:
            raise ValueError('Wrong target parameter passed')

        # formatters
        if format == 'csv':
            self.formatter = lambda row : ','.join([ str(i) for i in row ]) + "\n"
        elif format == 'table':
            self.formatter = lambda row : row  # TODO implement a pretty-printer
        else:
            raise ValueError('Wrong format is passed: ' + format)


    def write(self, row=[]):
        line = self.formatter(row)
        self.target.write(line)

    def close(self):
        self.target.close
        return
