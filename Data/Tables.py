from numpy import zeros, dtype
from functools import partial

class Table(object):
    def __init__(self, tokens):
        self.tokens = tokens.tokens
        dim = tokens.S
        self.array = zeros((dim, dim), dtype=float)

    # simple tables
    def build_table(self, attribute, join=None):
        """Simple tables : takes an attribute of key:value type, where
        key: tokenid, value: value in relation to the referring token;
        builds a table as token X token with the referring value in the cell."""

        if join:
            return self._joined_tables(attribute, join)

        for xToken in self.tokens:
            yTokens = ''
            try:
                # print(attribute)
                # print (xToken)
                yTokens = getattr(xToken, attribute)
                # print (yTokens)
            except:
                raise ValueError

            x = xToken.idx
            print (yTokens)
            for y, v in yTokens.items():
                self.array[x][y] = v


    def _joined_tables(self, attribute, join):
        for xToken in self.tokens:
            v1 = 0.0
            try:
                fun = partial(getattr(t, attribute), x)  # partial function -> no check we have on parameters!
            except:
                raise ValueError(e)
            x = xToken.idx
            for yToken in getattr(t, join):  # this is an iterable on which we calculate the actual formula
                y = yToken.idx
                self.array[x][y] = fun(yToken)

# NOTES: if we can Curry the calculation in the external loop we can optimize the calculation in the internal loop
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
