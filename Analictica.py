from aConfig import Config
from Source import Corpus
from Data.Elements import Elements
from Data import Tables

from testHelpers import *

Config = Config()


elements = Elements(datasource=Corpus(source='ATU_Motifchain').tokenize_source())
elements.sentences.add_co_occurrences(elements.tokens)  # XXX this could be hooked into token processing

# recall_text(elements)
# print_tokens(elements.tokens)
# print_PMI(elements.tokens)

table = Tables.Table(elements.tokens)
print(table.build_table(method='co_occurrence'))

print (table.build_table(method='PMI'))
#
# table.build_table(method='PMI')
print(table.write_formatted())


from Engines import Yuret
Yur = Yuret(elements.tokens)  # initialize the engine with the primal dataset

[ Yur.process_sentence(s) for s in elements.sentences.get_sentences() ]  # process the dataset. Yes, we can make it iter as we did with Elements




