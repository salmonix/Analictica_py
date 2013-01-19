from Data.Elements import Elements
from Source import Readin
from NLP.Tokenizers import Tokenizer, Sentencer
from NLP.Filters import Stopword

# environment sanity checks
import sys

if sys.version_info >= (3,0):
    print ('NLTK at the moment runs with the version 2.x')
    sys.exit(1)
    

# get what I want to read from
data = { 'test' : 'txt' } 


# read it in aggregating into a pile -> source : [ sentences ]
source = Readin()
source_iterator = source.read_data( **data )
sentencer = Sentencer( sentencer='punkt', language='english' )
tokenizer = Tokenize( tokenizer='PunktWord', language='english' )


elements = Elements()
for title, data in source_iterator():
    texts.text(source)
    for i in data:
        tokens=sentencer.process(i)
        text.add_token_idx( tokenizer.get_tokens( data ) )


# make transform module -> from the token hash to create frequency and other tables and stats
# from text to create a graph ( inserting sequence data into the token hash )


# TODO: use listst wherever possible
