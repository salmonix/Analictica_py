from Data.Elements import Tokens

def get_engine(name, elements):
    if name == 'Yuret':
        pass
    raise ValueError(name + 'is not implemented')


class Yuret(object):

    def __init__(self, tokens):
        self.link_candidates = []
        self.links = Tokens()  # we collect the links into an elements list. Always the lower tokenid is used
        self.tokens = tokens

    def process_sentence(self, data):  # takes a sentence list
        end = len(data)
        links = []
        stack_pmi = 0
        cycle_pointer = 0
        # tokens = self.tokens.tokens

        links.append((0, 1))  # initial state for the links stack

        for l in range(0, end):  # take the right element of the link

            for r in range(l + 1, end):

                stack = []  # stack is for storing the ok links
                cycle_pointer = 0
                print ("\nLooking for link : %d %d " % (l, r) + ' against links:' + str(links).strip('[]'))

                for link in links:  # iterate on the links stack

                    if link[0] == cycle_pointer:
                        cycle_pointer = link[1]

                    print("\n    Link element : " + str(link).strip('[]'))
                    print('    Cycle pointer %d' % (cycle_pointer))
                    if cycle_pointer == r:  # we have a cycle
                        # stack = self.manage_cycle((l, r), PMI, stack, stack_pmi, left)
                        print ("    --> Cycle detected - cycle_pointer %d -> link( %d, %d )  ->overwrite" % (cycle_pointer, l, r))
                        continue

                    if link[0] < l and link[1] < r:
                        # stack = self.manage_Xlink((l, r), PMI, stack, stack_pmi, left)
                        print ("    --> Xlink detected as %d < %d and %d < %d   -> overwrite" % (link[0], l, link[1], r))
                        continue

                    stack.append(link)  # if we are here -> left is ok.
                    print ('    Neither cycle nor Xlink found -> link added to stack ' + str(stack).strip('[]'))

                else:
                    # stack.reverse()
                    links = stack + [(l, r)]
                    print ('EOL: stack + (%d,%d) -> Links:' % (l, r) + str(links).strip('[]'))

        # self.store_links(left_links)

        print ("\n### Finally LINKS:" + str(links).strip('[]'))


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

