from Data.Elements import Elements
from Source import Readin
from NLP.Tokenizers import Tokenizer, Sentencer
from NLP.Filters import Stopword

# environment sanity checks
import sys

if sys.version_info >= (3,0):
    print ('NLTK at the moment runs with the version 2.x')
    sys.exit(1)

def process_source(source,language,sentencer,tokenizer):

    source_iterator = Readin().read_data( source )
    sentencer = Sentencer( sentencer, language )
    tokenizer = Tokenizer( tokenizer, language )
    elements = Elements()

    for title, data in source_iterator:
        for i in data:
            sentences=sentencer.process(i) 
            for s in sentences:
                tokens = tokenizer.get_tokens(s)
                elements.add_data( title, tokens )

    return elements

# TODO make transform module -> from the token hash to create frequency and other tables and stats
# from text to create a graph ( inserting sequence data into the token hash )

elements = process_source( sentencer = 'punkt',language='english', tokenizer='PunktWord', source='test')
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
