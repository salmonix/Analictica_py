from Source import Corpus
from Data.Elements import Elements
from Modules.Abacus import *
# environment sanity checks
import sys

def test_for_text_tokens(elements): # this is the way to iterate over the corpus
    texts = elements.texts
    tokens = elements.tokens
    text_iter = texts.get_sentences() 
    a = ''
    for sentences in text_iter:
        print sentences
        print tokens.tokens
        for s in sentences:
            print (tokens.tokens[s]['name']) # XXX sg goes wrong


elements = Elements( sentencer = 'punkt',language='english', tokenizer='PunktWord')
for (title, text ) in Corpus().process( source = 'test' ): # I feel it awkward
    elements.process_datastring(title,text)


elements.tokens.add_entropy('shannon')
# print('Sorting test')
# ordered_elements = elements.tokens.order('shannon') # this is an array
# test_for_text_tokens(elements)

co_occ=co_occurrence_table(elements)
joined_probab = joined_probability_table(co_occ, elements.tokens)
mgtable = mutual_gain_table( joined_probab, elements.tokens )
