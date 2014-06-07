from numpy import zeros, dtype
from functools import partial
import sys

from WriteMatrices import WriteTable

class Table(object):

    def __init__(self, tokens):
        self.tokens = tokens


    # XXX the indexing method is bad. If we remove an element the indexing should also move,
    # so we should build an internal lookup _first_. This should be an object because I guess
    # the problem is more general that this module.
    # simple tables
    def build_table(self, method):
        """Simple tables : takes an attribute of key:value type, where
        key: tokenid, value: value in relation to the referring token;
        builds a table as token X token with the referring value in the cell.
        If the method is callable, then it supposedly is some kind of joined method ( eg. joined probability )
        and the attribute co_occurrence is used assuming that it contains the relevant data - eg. co_occurrence with other
        tokens, in a dictionary. So, it is used instead of iterating over token x token times and letting each token
        run this check internally."""
        dim = len(self.tokens)  # space starts from 1, lists from 0
        table = zeros((dim, dim), dtype=float)  # the given tablespace is always overwritten

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
                         table[x][y] = v
                except:
                    ne xt

            elif hasattr(yMethod, '__call__'):  # callable
                try: 
                    fun = partial(yMethod)  # not faster but clearer
                except:
                    raise ValueError('Unable to get partial function from method ' + str(method))

                # print ('Indexes: ' + str(x) + ' : ' + str(xToken.co_occurrence))

                for yTokenId in xToken.co_occurrence.keys():
                    y = self.tokens[yTokenId].idx
                    table[x][y] = fun(self.tokens[yTokenId])

            else:  # attribute - make it ordered.
                for yTokenId in xToken.co_occurrence.keys():
                    y = self.tokens[yTokenId].idx
                    table[0][x] = yMethod

        self.table = table
        return table 


    def write_formatted(self, **kwargs):  # takes also : target object
        # if there is not table -> formatting must fail instead of creating an empty table
        # it will not work with ARRAYs  - we must write it immediately out to the passed object

        writer = WriteTable(**kwargs)
        header = [ t.name for t in self.tokens]
        writer.write(header)

        for i in range(1, len(header)):
            row = []
            row.append(header[i])
            for e in self.table[i - 1]:
                row.append(e)
            writer.write(row)

        writer.close()
        return 1  # deal with the error cases



