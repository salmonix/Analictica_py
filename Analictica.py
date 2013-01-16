import NLP
import Elements
import Source

# get what I want to read from
data = { 'test' : 'txt' } 


# read it in aggregating into a pile -> source : [ sentences ]
source = Source()
source_iterator = source.read_data( data )

elements = Elements()
for title, data in source_iterator():
    texts.text(source)
    for i in data:
        text.add_token_idx( tokenizer.add_token( data ) )


# make transform module -> from the token hash to create frequency and other tables and stats
# from text to create a graph ( inserting sequence data into the token hash )


# TODO: use listst wherever possible
