from aConfig import Config
from Source import Corpus
from Data.Elements import Elements
from Representations import Tables
from Representations.Graph import make_graph_with_attribute
import networkx as nx

from testHelpers import *

Config = Config()


elements = Elements(datasource=Corpus(source='ATU_Motifchain').tokenize_source())
# elements = Elements(datasource=Corpus(source='test').tokenize_source())
elements.sentences.add_co_occurrences(elements.tokens)  # XXX this could be hooked into token processing

# raw_input('RECALL TEXT')
# recall_text(elements, by='name')
# raw_input('TOKENS ELEMENTS')
# print_tokens(elements.tokens)
# raw_input('PMI')
# print_PMI(elements.tokens)

table = Tables.Table(elements.tokens)
table.build_table(method='co_occurrence')
table.write_formatted(file='Co-occ.csv', format='csv')

table.build_table(method='PMI')
table.write_formatted(file='PMI.csv', format='csv')


from Engines import Yuret
Yur = Yuret(elements.tokens)  # initialize the engine with the primal dataset

link_graph = nx.Graph()
text_graph = nx.DiGraph()

for s in elements.sentences.get_sentences_by_object():

   Yur.process_sentence(s)
   link_graph = Yur.as_graph(link_graph)

   text_graph = make_graph_with_attribute(text_graph, s)

nx.write_gexf(link_graph, '../Link_graph.gexf', encoding='utf-8', prettyprint='True')
nx.write_gexf(text_graph, '../Text_graph.gexf', encoding='utf-8', prettyprint='True')
