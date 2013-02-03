from numpy import zeros, dtype
from functools import partial

class Table(object):
    def __init__(self, tokens):
        self.tokens = tokens.tokens
        dim = tokens.S
        self.array = zeros((dim, dim), dtype=float)

    # simple tables
    def build_table(self, method):
        """Simple tables : takes an attribute of key:value type, where
        key: tokenid, value: value in relation to the referring token;
        builds a table as token X token with the referring value in the cell."""

        for xToken in self.tokens:
            yTokens = ''
            try:
                # print(attribute)
                # print (xToken)
                yTokens = getattr(xToken, method)
                # print (yTokens)
            except:
                raise ValueError

            x = xToken.idx
            print (yTokens)

            if hasattr(yTokens, '__iter__'):
                for y, v in yTokens.items():
                    self.array[x][y] = v

            elif hasattr(yTokens, '__call__'):
                try:
                    fun = partial(getattr(xToken, method))  # partial function -> no check we have on parameters!
                except:
                    raise ValueError('Unable to get partial function from method ' + str(method))
                for yToken in self.tokens:  # this is an iterable on which we calculate the actual formula
                    y = yToken.idx
                    self.array[x][y] = fun(yToken)

            else:
                raise ValueError('Parameter method returns neither iterable nor function.')


    def write_formatted(self):  # takes also : target object
        # if there is not table -> formatting must fail instead of creating an empty table
        # it will not work with ARRAYs  - we must write it immediately out to the passed object
        target = []
        header = [ t.name for t in self.tokens.tokens]
        target.append(header)
        # target.write(header)
        self.array.instert(0, header)
        for i in range(0, len(header)):
            target.append(header[i], self.array[i])
            # target.write(header[i], self.array[i])

        return target
