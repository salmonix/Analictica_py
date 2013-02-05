from Source import Corpus
from Data.Elements import Elements
from Modules.Abacus import *
from Data import Tables

import sys
from pprint import pprint

def test_for_text_tokens(elements):
    texts = elements.sentences
    tokens = elements.tokens
    text_iter = texts.get_sentences()
    for sentences in text_iter:
        for s in sentences:
            print ("token id :" + str(s))
            print (tokens.tokens[s].name)

def print_tokens(tokens):
    for t in tokens.tokens:
        print('name: ' + t.name + ' | idx: ' + str(t.idx) + ' | freq: ' + str(t.freq) + ' | S: ' + str(t.Space))
        print('co_occurrence' + str(t.co_occurrence))
        print('prob.: ' + str(t.probability) + ' entropy: ' + str(t.shannon) + "\n")


elements = Elements(sentencer='punkt', language='english', tokenizer='PunktWord')
for (title, text) in Corpus().process(source='test'):  # I feel it awkward
    elements.process_datastring(title, text)

elements.sentences.add_co_occurrences(elements.tokens)  # XXX this could be hooked into token processing
# test_for_text_tokens(elements)
print_tokens(elements.tokens)
table = Tables.Table(elements.tokens)
print (table.build_table(method='co_occurrence'))
print (table.build_table(method='PMI'))

print(table.write_formatted())
