from aConfig import Config
from Source import Corpus
from Data.Elements import Elements
from Data import Tables

import networkx as nx

from testHelpers import *

Config = Config()


# elements = Elements(datasource=Corpus(source='ATU_Motifchain').tokenize_source())
elements = Elements(datasource=Corpus(source='test').tokenize_source())
elements.sentences.add_co_occurrences(elements.tokens)  # XXX this could be hooked into token processing

# raw_input('RECALL TEXT')
# recall_text(elements)
# raw_input('TOKENS ELEMENTS')
# print_tokens(elements.tokens)
# raw_input('PMI')
# print_PMI(elements.tokens)

# table = Tables.Table(elements.tokens)
# print(table.build_table(method='co_occurrence'))

# print (table.build_table(method='PMI'))
#
# table.build_table(method='PMI')
# table.write_formatted(file='PMI.csv', format='csv')


from Engines import Yuret
Yur = Yuret(elements.tokens)  # initialize the engine with the primal dataset

link_graph = nx.Graph()
text_graph = nx.DiGraph()
combined_graph = nx.Graph()

# we must check for the existence of the given graph

def make_graph(sequence, a_graph):
    sequence = [text_graph.add_nodes(tokens[t].real_name) for t in sequence]

    prev = ''
    prev_name = ''
    for t in sequence:
        token = tokens[t]
        token_name = token.name

        a_graph.add_node(token_name, pmi=token.pmi)

        if prev:
            a_graph.add_edge(prev_name, token_name)  # so, we need to add attributes to the link, that is increment the mutual co-occurrence
            a_graph.edge[ prev_name ][ token_name ].weight += 1
            prev = token
            prev_name = token.name



def graph_from_linksequence(sequence, a_graph):

    prev = ''
    prev_name = ''
    for t in sequence:
        token = tokens[t]
        token_name = token.name

        a_graph.add_node(token_name, pmi=token.link_PMI)

        if prev:
            a_graph.add_edge(prev_name, token_name)
            a_graph.edge[ prev_name ][ token_name ].weight += 1
            prev = token
            prev_name = token.name



for s in elements.sentences.get_sentences():
    linked_sentence = Yur.process_sentence(s)
    make_graph(s, text_graph)
    graph_from_linksequence(linked_sentence, link_graph)


text_graph.write_gml('../Text_graph.gml')
graph_from_linksequence.write_gml('../Links_graph.gml')
