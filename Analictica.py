from Source import process_sources

# environment sanity checks
import sys

def test_for_text_tokens(elements):
    texts = elements.texts
    tokens = elements.tokens
    text_iter = texts.get_text() 
    a = ''
    for t in text_iter:
        sentences = t[1]
        for s in sentences:
            for i in s:
                a = a + ' ' + tokens.tokens[i]['name']
    print a


elements = process_sources( sentencer = 'punkt',language='english', tokenizer='PunktWord', source='test')
elements.tokens.add_entropy('shannon_entropy')
print('Sorting test')
ordered_elements = elements.tokens.order('shannon_entropy')
print ordered_elements


