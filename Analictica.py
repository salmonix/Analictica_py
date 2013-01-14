import NLP
import Elements.Texts
import Element.Tokenlist

# get what I want to read from
data = { 'test' : 'txt' } 


# read it in aggregating into a pile -> source : [ sentences ]
source = Source()
source_iterator = source.read_data( data )

tokens = Elements.Tokenlist()
texts = Elements.Textlist

# tokenize it ( a parameter can be a filter object to sort out noise )
# tokenizer = NLP.Tokenizer( )

while title, data = source_iterator.next():
    texts.text(source)
    data = tokenizer.process(data)
    for i in data:
        text.add_token_idx( tokenizer.add_token( i ) )


# make transform module -> from the token hash to create frequency and other tables and stats
# from text to create a graph ( inserting sequence data into the token hash )


# TODO: use listst wherever possible
