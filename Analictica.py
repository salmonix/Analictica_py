from Source import Corpus
from Data.Elements import Elements

# environment sanity checks
import sys

def test_for_text_tokens(elements):
    texts = elements.texts
    tokens = elements.tokens
    text_iter = texts.get_text() 
    a = ''
    for t in text_iter:
        sentences = t[1] # it is a title - sentences tuple
        for s in sentences:
            print s
#            for i in s: # token level
#                print (tokens.tokens[i]['name']) # XXX sg goes wrong


elements = Elements( sentencer = 'punkt',language='english', tokenizer='PunktWord')
for (title, text ) in Corpus().process( source = 'atu' ): # I feel it awkward
    elements.process_datastring(title,text)


elements.tokens.add_entropy('shannon')
# print('Sorting test')
# ordered_elements = elements.tokens.order('shannon') # this is an array
test_for_text_tokens(elements)
