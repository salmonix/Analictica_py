# import unittest
from Engines import Yuret
from Data.Elements import Elements
from pprint import pprint
import sys





def print_tokens(tokens):
    for t in tokens.tokens:
        print('name: ' + t.name + ' | idx: ' + str(t.idx) + ' | freq: ' + str(t.freq) + ' | S: ' + str(t.Space))
        print('co_occurrence' + str(t.co_occurrence))
        print('prob.: ' + str(t.probability) + ' entropy: ' + str(t.shannon) + "\n")


# build the 'sentences' we pass to the engine
Elements = Elements()
data = [
        [0, 1, 2, 3, 2, 3, 1, 1, 4, 3, 2, 4],
        [0, 2, 2, 4, 3, 4, 4, 2, 3, 1, 3, 2]
        ]
[ Tok.add_token(d) for d in data ]  # add tokens

print_tokens(Tok)

print(Tok.tokens[0].PMI(Tok.tokens[2]))

Yur = Yuret(Elements.tokens)  # initialize the engine with the primal dataset

[ Yur.process_sentence(d) for d in data ]  # process the dataset

# here get the results...


