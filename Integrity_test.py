from Configuration import Corpora
from Source import Corpus
from Elements import Elements
from Representations import Table
from Representations.Graph import make_graph_with_attribute
import networkx as nx
from pprint import pprint
from Utils.File import write_file, file_slurp

from testHelpers import *
import sys
import logging
logging.basicConfig(stream=sys.stderr, format='%(message)s', level=logging.DEBUG)


Config = Corpora()  # initialize the a configuration instance

"""This package is to run the new features on  a gives test set with all the unique parameters and outputs.
The purpose of this program at the moment is to prove that the units are ok when glued together."""

# print('to index: %i' % len(filterwords['to_index']))

data_corpus = '10tales'

elements = Elements(datasource=Corpus(source=data_corpus).tokenize_source())
print(len(elements.tokens))
# assert len(elements.tokens) ==


# elements = Elements(datasource=Corpus(source=data_corpus).tokenize_source(stopwords=filterwords['to_stop']))

# TODO: this could be hooked into token processing
# so we do not have to parse the whole story through again.
# elements.sentences.add_co_occurrences(elements.tokens)

# raw_input('RECALL TEXT')
# recall_text(elements, by='name')
# raw_input('TOKENS ELEMENTS')
# print_tokens(elements.tokens)
# raw_input('PMI')
# print_PMI(elements.tokens)

# table = Table( elements.tokens.tokens)
# table.build_table(method='IC')
# table.write_formatted(file='../IC.csv', format='csv') # we may also guess it...

# table.build_table(method='PMI')
# table.write_formatted(file='PMI.csv', format='csv')

# subset = elements.tokens.get_subset_by_attribute({'name' : ['a', 'b'] })

# subset = elements.tokens.get_subset_by_attribute({'name' : filterwords['to_index'] })
#
#
# subset = set([ x.name for x in subset ])
# for e in filter_words['to_index']:
#     if e not in subset:
#         print "Not found" + e


# from Engines import Yuret
# Yur = Yuret(elements.tokens)  # initialize the engine with the primal dataset
#
# # link_graph = nx.Graph()
# # text_graph = nx.DiGraph()
#
# counter = 0
# for title, s in elements.sentences.get_sentences_by_object():
#     if len(s) < 2:
#         continue
#     logging.info("\n -----------> TEXT: " + title)
#     Yur.process_sentence(s)
#     link_graph = Yur.as_graph()
#
#     # text_graph = make_graph_with_attribute(text_graph, s)
#     nx.write_gexf(link_graph, '../ATU_4xx/' + title + '_link_graph.gexf', encoding='utf-8', prettyprint='True')


# nx.write_gexf(text_graph, '../Text_graph.gexf', encoding='utf-8', prettyprint='True')
