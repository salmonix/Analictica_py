from Data import Tokens

def get_engine(name, elements):
    if name == 'Yuret':
        return Trainee(elements)
    raise ValueError(name + 'is not implemented')


class Yuret(object):

    def __init__(self, tokens):
        self.link_candidates = []
        self.links = Tokens()  # we collect the links into an elements list. Always the lower tokenid is used
        self.tokens = tokens


    def process_sentence(data):  # takes a sentence list
        end = len(data) - 1
        left_links = []

        for r in range(0, end):  # take the right of the link
            curr = tokens[ data[p] ]

            for l in range(p - 1, 0):  # iterate the left of the link

                PMI = curr.PMI(tokens[ data[l] ])  # get the mutual information content with the token on the left

                if PMI < 0 :  # negative links no accepted
                    if p == 0 :  # we are at the end of the sentence
                         self.store_links(links)
                    continue

                for left in left_links:  # X links
                    if left[0] < l and left[1] > l:
                        self.manage_Xlink(left, (l, r))
                        # XXX ?



    def store_links(self, links=[]):
        pass

    def manage_Xlink(self, left, current):
        pass
