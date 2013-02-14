from Data.Elements import Tokens

def get_engine(name, elements):
    if name == 'Yuret':
        return Trainee(elements)
    raise ValueError(name + 'is not implemented')


class Yuret(object):

    def __init__(self, tokens):
        self.link_candidates = []
        self.links = Tokens()  # we collect the links into an elements list. Always the lower tokenid is used
        self.tokens = tokens

    def process_sentence(self, data):  # takes a sentence list
        end = len(data) - 1
        left_links = []
        stack = []
        cycle_pointer = 0
        stack_pmi = 0
        # tokens = self.tokens.tokens

        for r in range(1, end):  # take the right element of the link
            print ("%d is right" % (r))

            for l in range(r - 1, end):  # the nested all with all loop

                print ("%d is left" % (l))
                for left in left_links:  # iterate on the left_links stack
                    PMI = 1
                    # PMI = tokens[l].PMI(tokens[r])
                    # if PMI < 0 :  # negative links no accepted
                    #   if p == 0 :  # we are at the end of the sentence
                    #       self.store_links(links)
                    # continue

                    if cycle_pointer == l:  # we have a cycle
                        self.manage_cycle((l, r), PMI, stack, stack_pmi, left)
                        continue

                    if left[0] < l and left[1] > l:
                        self.manage_Xlink((l, r), PMI, stack, stack_pmi, left)
                        continue

                    if left[1] < l:
                        left_links.append((l, r))
                        break

                    if left[1] == cycle_pointer:
                        cycle_pointer = left[0]

                    stack.append(left)
                    stack_pmi += PMI

                    left_links.append((l, r))
                    # problems: 1 we have multiple entries - a link that exists turns up several times
                    # I see not that it enters the cycle and Xlink managers
                    # we do not delete the Xlinks and Cycles at this point -> TODO

        self.store_links(left_links)


    def store_links(self, links=[]):
        pass
        link_tokens = self.links
        for link in links:
            # idx = link_tokens.add_token(link[0])
            # link_tokens.tokens[idx].aux = link[1]
            print "LINKS"
            print(links)


    # in these case we need the PMI of the stock against the current PMI to make a decision
    # both methods are the same and might apply the same logic
    def manage_Xlink(self, current, PMI, stack, stack_pmi, left):
        print 'Xlinks:'
        print current
        print stack
        print left
        pass

    def manage_cycles(self, current, PMI, stack, stack_pmi, left):
        print 'Cycles:'
        print current
        print stack
        print left
        pass

