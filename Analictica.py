from Configuration import Corpora
from Source import Corpus
from Elements import Elements
from Representations import Table
from Representations.Graph import make_graph_with_attribute
import networkx as nx
from pprint import pprint

from testHelpers import *
import sys
import logging
logging.basicConfig(stream=sys.stderr, format='%(message)s', level=logging.DEBUG)


# TODO: Create an overall documentation

Config = Corpora()

import yaml

filter_words = None
with open('/home/salmonix/DARANYI_MOTYO/LEGUJABB/10Tales_1st_wordlist.yml', 'r') as f:
     filter_words = yaml.load(f)

elements = Elements(datasource=Corpus(source='10tales').tokenize_source(stopwords=filter_words['to_stop']))

# elements = Elements(datasource=Corpus(source='ATU_Motifchain').tokenize_source())
# elements = Elements(datasource=Corpus(source='test').tokenize_source())

# XXX this could be hooked into token processing
# so we do not have to parse the whole story throught again.
# TODO: I guess sentences are only a hierarchy of sequences, so it should be rewritten
elements.sentences.add_co_occurrences(elements.tokens)

# pprint (elements.tokens.tokens)

# subset = elements.tokens.get_subset_by_attribute({'name' : ['a', 'd'] })


# raw_input('RECALL TEXT')
# recall_text(elements, by='name')
# raw_input('TOKENS ELEMENTS')
# print_tokens(elements.tokens)
# raw_input('PMI')
# print_PMI(elements.tokens)

table = Table(elements.tokens.tokens)
table.build_table(method='IC')
table.write_formatted(file='../IC.csv', format='csv')

table.build_table(method='PMI')
table.write_formatted(file='PMI.csv', format='csv')

# param = { }
# subset = elements.tokens.get_subset_by_attribute({'name' : ['a', 'b'] })


subset = elements.tokens.get_subset_by_attribute({'name' : filter_words['to_index'] })

# pprint(subset)


from Engines import Yuret
Yur = Yuret(elements.tokens)  # initialize the engine with the primal dataset
#
link_graph = nx.Graph()
text_graph = nx.DiGraph()
#
counter = 0
for title, s in elements.sentences.get_sentences_by_object():
    if len(s) < 2:
        continue
    logging.info("\n -----------> TEXT: " + title)
    Yur.process_sentence(s)
    link_graph = Yur.as_graph()
    text_graph = make_graph_with_attribute(text_graph, s)
    nx.write_gexf(link_graph, '../ATU_4xx/' + title + '_link_graph.gexf', encoding='utf-8', prettyprint='True')


nx.write_gexf(text_graph, '../Text_graph.gexf', encoding='utf-8', prettyprint='True')
