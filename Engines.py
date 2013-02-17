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
        # tokens = self.tokens.tokens

        c = 0
        links = [(0, 1)]
        for r in range(1, end):  # take the right element of the link

            for l in range(r, -1, -1):  # the lookback loop

                if not links:
                    print ('left_links is empty, so we add %d %d if PMI is positive -> next' % (l, r))
                    print('We shall not be here, anyway...')
                    links.append((l, r))
                    continue

                stack = []

                print ("\nLooking for link : %d %d " % (l, r) + '   against links:' + str(links).strip('[]'))
                cycle_pointer = links[0][1]
                print('Initial cycle_pointer %d' % (cycle_pointer))

                for link in links:  # iterate on the links stack

                    print("\n   Left link element : " + str(link).strip('[]'))

                    if cycle_pointer == r:  # we have a cycle
                        # stack = self.manage_cycle((l, r), PMI, stack, stack_pmi, left)
                        print ("    ->Cycle detected %d : %d  ->overwrite" % (l, r))
                        continue

                    if link[0] < r and link[1] > r:
                        # stack = self.manage_Xlink((l, r), PMI, stack, stack_pmi, left)
                        print ("    ->Xlink detected %d : %d   -> skip" % (l, r))
                        continue

                    # ciklus mutato nem valtozik !!
                    if link[0] == cycle_pointer:
                        cycle_pointer = link[1]

                    stack.append(link)  # if we are here -> left is ok.
                    print ('  Neither cycle nor Xlink found ->')
                    print ('    Cycle pointer: %d ' % (cycle_pointer))
                    print ('    Stack:' + str(stack).strip('[]'))

                else:
                    # stack.reverse()
                    links = stack + [(l, r)]
                    print (' Stack:' + str(stack).strip('[]'))
                    print (' apply stack to left_links:  LINKS:' + str(links).strip('[]'))

        # self.store_links(left_links)
        print ('Finally LINKS:' + str(links).strip('[]'))



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

