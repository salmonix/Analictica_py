from Data import Links

def get_engine(name, elements):
    if name == 'Yuret':
        return Trainee(elements)
    raise ValueError(name + 'is not implemented')


class Yuret(object):

    def __init__(self, tokens):
        self.link_candidates = []
        self.links = Links()  # we collect the links into an elements list. Always the lower tokenid is used
        self.tokens = tokens
        self.left_links = []
        self.stack = []  # it should be stack type


    def process_sentence(data):  # takes a sentence list
        end = len(data) - 1
        left_links = self.left_links  # list of tuples

        for r in range(1, end):  # take the right element of the link

            for l in range(r - 1, 0):  # the nested all with all loop


                for left in left_links:  # iterate on the left_links stack

                    if PMI < 0 :  # negative links no accepted
                        if p == 0 :  # we are at the end of the sentence
                            self.store_links(links)
                    continue

                    if left[1] == next_to_cycle:
                        next_to_cycle = left[0]

                    if next_to_cycle == l:  # we have a cycle
                        self.manage_cycle(stack , left, (l, r))
                        continue

                    if left[0] < l and left[1] > l:
                        self.manage_Xlink(stack, left, (l, r))

                    stack.append(left)

                left_links.append((l, r))


    def store_links(self, links=[]):

        self.stack = 'empty'
        pass

    def manage_Xlink(self, left, current):
        self.links[ left ][Xlink] = {current}

    def manage_cycles(self, cycle, current):
        self.links[ left ][Xlink] = {current}

