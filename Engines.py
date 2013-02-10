from Data import Tokens

def get_engine(name, elements):
    if name == 'Yuret':
        return Trainee(elements)
    raise ValueError(name + 'is not implemented')


class Yuret(object):

    def __init__(self,):
        self.link_candidates = []
        self.links = Tokens()  # we collect the links into an elements list. Always the lower tokenid is used


    def process_sentence(data):  # takes a sentence list
        end = len(data) - 1
        sentence_graph = {}  #
        tokens = self.tokens
        p = 1  # position in the sentence
        sp = 0  # stack pointer for the stack of links

        while 1:  # take the current element
            cycle = True  # initial value for the cycle
            curr = tokens[ data[p] ]
            while 1:  # check to the left
                l = p - 1
                PMI = curr.PMI(tokens[l])  # get the mutual information content with the token on the left

                if PMI < 0 :  # negative links no accepted
                    if p == 0 :
                         break
                    continue

                if p - 1 != l:  # detect cycles and X loops: we walk to l from p -> if possible, it is a cycle
                    if p in sentence_graph:
                        paths = sentence_graph[p]




