from aConfig import Config
from Source import Corpus
from Data.Elements import Elements
from Data import Tables

import networkx as nx

from testHelpers import *

Config = Config()


elements = Elements(datasource=Corpus(source='ATU_Motifchain').tokenize_source())
elements.sentences.add_co_occurrences(elements.tokens)  # XXX this could be hooked into token processing

# recall_text(elements)
# print_tokens(elements.tokens)
# print_PMI(elements.tokens)

table = Tables.Table(elements.tokens)
# print(table.build_table(method='co_occurrence'))

# print (table.build_table(method='PMI'))
#
table.build_table(method='PMI')
table.write_formatted(file='PMI.csv', format='csv')


# from Engines import Yuret
# Yur = Yuret(elements.tokens)  # initialize the engine with the primal dataset

link_graph = nx.Graph()
text_graph = nx.Graph()  # diGraph ?
combined_graph = nx.Graph()

def make_graph(sequence, a_graph):
    sequence = [text_graph.add_nodes(tokens[t].real_name) for t in sequence]

    for i in range(0, len(sequence)):
        a_graph.add_edge(sequence[i], sequence[i + 1])  # so, we need to add attributes to the link, that is increment the mutual co-occurrence
        a_graph.edge[sequence[i]][ sequence[i + 1]].weight += 1


# ? what is the attribute structure here? what do I want to see?
def graph_from_linksequence(sequence, a_graph):

    prev = ''
    for t in sequence:
        name = (tokens[t].real_name)
        PMI = tokens[t].link_PMI
        a_graph.add_nodes(name, pmi=PMI)
        if prev:
            a_graph.add_edge(prev.name, name)
            a_graph.edge[prev.name][ name ].weight += 1
            prev = tokens[t]



for sentence in elements.sentences.get_sentences():
    linked_sentence = Yur.process_sentence(s)
    make_graph(s, text_graph)
    graph_from_linksequence(linked_sentence, link_graph)





