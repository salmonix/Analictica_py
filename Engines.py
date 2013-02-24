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
        # links are: ( l, r, link_value ), where: l - r are positional values in data list, link_value is the calculated pmi.
        links = []
        cycle_pointer = 0
        tokens = self.tokens.tokens
        stringit = lambda x : str(x).strip('[]')

        print('Sentence received : ' + stringit(data))

        links.append((0, 1))  # initial state for the links stack

        for r in range(2, end):  # take the right element of the link
            right = tokens[ data[r]]
            for l in range(r - 1, 0, -1):

                link_value = right.PMI(tokens[ data[r]])
                if link_value <= 0:
                    continue

                print ("\n  Looking for link : %d %d " % (l, r) + ' against links:' + stringit(links))
                Xlinks = []
                Cycles = []
                cycle_pointer = None
                stack = []  # actual storage because we do not want to change 'links' in the loop

                for link in links:  # iterate on the links stack

                    if  link[0] < l and link[1] <= l:  # out of our present investigation window
                        # print('# Found out of range link' + str(link))
                        print('    append good link %s' % (stringit(link)))
                        stack.append(link)  # good links
                        continue

                    # first check for Xlinks -> Xlink can be a start of the cycle
                    if link[0] < l and link[1] > l and link[1] < r:
                        print ("    ---> Xlink detected as %d < %d and %d < %d   -> stackin'" % (link[0], l, link[1], r))
                        Xlinks.append(link)
                        continue

                    if Xlinks:
                        print("     ----> make an Xlink decision on " + stringit(Xlinks))
                        print("      ----> sum(stack) cmp l")
                        sum_stack = sum(Xlink[2] for Xlink in Xlinks)  # this is the stack PMI-> sum of link PMIs
                        print("         SUM(Xlinks): %d    link value: %d" % (sum_stack, r - l))
                        if link_value > sum_stack:  # stronger link: drop the others, keep this
                            Xlinks = None
                        else:
                            print('      ----> Link is BAD link : keeping all unchanged: ' + stringit(links))
                            break  # this is a bad link

                    # check for Cycles
                    if cycle_pointer == link[0] or link[0] == l:
                        print("\n   Set cycle pointer as " + str(link[1]) + ' using stored link: ' + str(link))
                        cycle_pointer = link[1]
                        Cycles.append(link)
                        continue
                    else:
                        print('   Cycle pointer ' + str(cycle_pointer))

                    print("\n    Link element : " + stringit(link) + ' && cycle_pointer ' + str(cycle_pointer))

                    stack.append(link)

                else:  # evaluate

                    if cycle_pointer == r:  # check for cycle
                        print ("    --> Cycle detected - cycle_pointer %d -> link( %d, %d )  -> decide" % (cycle_pointer, l, r))
                        sum_stack = sum(cyc[2] for cyc in Cycles)
                        print("         SUM(Cycles): %d    link value: %d" % (sum_stack, link_value))
                        if link_value < sum_stack:  # bad link
                            print('      ----> Link is BAD link : keeping stack + Cycles : %s + %s' % (stringit(stack), stringit(Cycles)))
                            stack = stack + Cycles
                        else:
                            print('      ----> link is kept, Cycles  %s dropped' % (stringit(Cycles)))
                            links = stack + [(l, r, link_value)]
                    else:  # no cycle
                        links = stack + [(l, r, link_value)]
                        print ("\nEOL: Links %s + (%d,%d). -> %s " % (stringit(stack), l, r, stringit(links)))

        print ("\n### Finally LINKS:" + stringit(links))
        self.store_links(links)


    def store_links(self, links=[]):
        link_tokens = self.links
        for link in links:
            # idx = link_tokens.add_token(link[0])
            # link_tokens.tokens[idx].aux = link[1]
            print "LINKS"
            print(links)
