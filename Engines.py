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
        tokens = self.tokens.tokens
        found_links = []

        links.append((0, 1))  # initial state for the links stack

        for r in range(2, end):  # take the right element of the link
            # right = tokens[ data[r]]
            for l in range(r - 1, 0, -1):

#                PMI = right.PMI( tokens[ data[l]] )
#                if PMI <=0:
#                    continue

                print ("\nLooking for link : %d %d " % (l, r) + ' against links:' + str(links).strip('[]'))
                accepted = []  # stack is for storing the ok links
                Xlinks = []
                stack = []  # actual storage -> links under consideration
                cycle_pointer = None

                for link in links:  # iterate on the links stack

                    if  link[0] < l and link[1] <= l:  # out of our present investigation window
                        # print('# Found out of range link' + str(link))
                        stack  .append(link)  # good links
                        continue

                    # first check for Xlinks
                    if link[0] < l and link[1] > l and link[1] < r:
                        print ("    --> Xlink detected as %d < %d and %d < %d   -> stackin'" % (link[0], l, link[1], r))
                        Xlinks.append(link)
                        continue

                    if Xlinks:
                        print ("     ----> make an Xlink decision on " + str(Xlinks).strip('[]'))
                        # after decision continue checking against links
                        # if older links are eliminated we still have to look for cycles with the new link

                    # if the new link fails on the second test we have to restore the eliminated Xlinks
                    # because the link is purely destructive

                    # check for Cycles
                    if cycle_pointer == link[0] or link[0] == l:
                        print("\n   Initialize cycle pointer as " + str(link[1]) + ' using first valid link: ' + str(link))
                        cycle_pointer = link[1]
                        cycle_item_counter = 1
                    else:
                        print('   Cycle pointer ' + str (cycle_pointer))

                    stack.append(link)
                    print("\n    Link element : " + str(link).strip('[]') + ' && cycle_pointer ' + str(cycle_pointer))
                    if cycle_pointer == r:  # we have a cycle
                        print ("    --> Cycle detected - cycle_pointer %d -> link( %d, %d )  -> decide" % (cycle_pointer, l, r))
                        # so here we do something with the stack -> change or keep
                        # if stack.pmi < PMI:
                        #     stack =[] # we will add l,r at the end ?
                        # else:
                        #   continue
                        continue


                else:  # evaluate
                    print('  Xlinks : ' + str(Xlinks))
                    links = accepted + [(l, r)]
                    print ("\nEOL: stack + (%d,%d) -> Links:" % (l, r) + str(links).strip('[]'))

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

