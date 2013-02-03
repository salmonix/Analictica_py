from Source import Corpus
from Data.Elements import Elements
from Modules.Abacus import *

import sys
from pprint import pprint

def test_for_text_tokens(elements):  # this is the way to iterate over the corpus
    texts = elements.sentences
    tokens = elements.tokens
    text_iter = texts.get_sentences()
    c = 0
    for sentences in text_iter:
        print (str(c) + ' -> ' + str(sentences))
        for s in sentences:
            print ("token id :" + str(s))
            print (tokens.tokens[s].name)  # XXX sg goes wrong

def print_tokens(tokens):
    for t in tokens.tokens:
        print('name: ' + t.name + ' | idx: ' + str(t.idx) + ' | freq: ' + str(t.freq) + ' | S: ' + str(t.Space))
        print('co_occurrence' + str(t.co_occurrence))
        print('prob.: ' + str(t.probability) + ' entropy: ' + str(t.shannon) + "\n")


elements = Elements(sentencer='punkt', language='english', tokenizer='PunktWord')
for (title, text) in Corpus().process(source='test'):  # I feel it awkward
    elements.process_datastring(title, text)

elements.sentences.add_co_occurrences(elements.tokens)
# test_for_text_tokens(elements)
print_tokens(elements.tokens)
