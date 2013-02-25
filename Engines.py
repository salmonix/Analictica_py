from Data.Elements import Tokens, Links
import sys
import logging

logging.basicConfig(stream=sys.stderr, format='%(message)s', level=logging.DEBUG)

def get_engine(name, elements):
    if name == 'Yuret':
        pass
    raise ValueError(name + 'is not implemented')


class Yuret(object):

    def __init__(self, tokens):
        self.link_candidates = []
        self.links = Links()  # we collect the links into an elements list. Always the lower tokenid is used
        self.tokens = tokens

    def process_sentence(self, data):  # takes a sentence list

        end = len(data)
        # links are: ( l, r, link_value ), where: l - r are positional values in data list, link_value is the calculated pmi.
        links = []
        cycle_pointer = 0
        tokens = self.tokens.tokens
        stringit = lambda x : str(x).strip('[]')

        logging.info('Sentence received : ' + stringit(data))

        links.append((0, 1))  # initial state for the links stack

        for r in range(2, end):  # take the right element of the link
            right = tokens[ data[r]]
            link_value = -1
            for l in range(r - 1, 0, -1):

                link_value = right.PMI(tokens[ data[r]])
                if link_value <= 0:
                    logging.info ('link_value is zero or negative: %f' % (link_value))
                    continue

                logging.info ("\n  Looking for link : %d %d %f " % (l, r, link_value) + ' against links:' + stringit(links))
                Xlinks = []
                Cycles = []
                cycle_pointer = None
                stack = []  # actual storage because we do not want to change 'links' in the loop

                for link in links:  # iterate on the links stack

                    if  link[0] < l and link[1] <= l:
                        logging.info('    append good link %s' % (stringit(link)))
                        stack.append(link)  # good links
                        continue

                    # first check for Xlinks -> Xlink can be a start of the cycle
                    if link[0] < l and link[1] > l and link[1] < r:
                        logging.info ("    ---> Xlink detected as %d < %d and %d < %d   -> stackin'" % (link[0], l, link[1], r))
                        Xlinks.append(link)
                        continue

                    if Xlinks:
                        logging.info("     ----> make an Xlink decision on " + stringit(Xlinks))
                        logging.info("      ----> sum(stack) cmp l")
                        sum_stack = sum(Xlink[2] for Xlink in Xlinks)  # this is the stack PMI-> sum of link PMIs
                        logging.info("         SUM(Xlinks): %f    link value: %f" % (sum_stack, r - l))
                        if link_value > sum_stack:
                            Xlinks = None
                        else:
                            logging.info('      ----> Link is BAD link : keeping all unchanged: ' + stringit(links))
                            break  # this is a bad link

                    # check for Cycles
                    if cycle_pointer == link[0] or link[0] == l:
                        logging.info("\n   Set cycle pointer as " + str(link[1]) + ' using stored link: ' + str(link))
                        cycle_pointer = link[1]
                        Cycles.append(link)
                        continue
                    else:
                        logging.info('   Cycle pointer ' + str(cycle_pointer))

                    logging.info("\n    Link element : " + stringit(link) + ' && cycle_pointer ' + str(cycle_pointer))

                    stack.append(link)

                else:  # evaluate

                    if cycle_pointer == r:  # check for cycle
                        logging.info ("    --> Cycle detected - cycle_pointer %d -> link( %d, %d )  -> decide" % (cycle_pointer, l, r))
                        # find the weakes of the cycle
                        weakest = (0, 0, 100)  # PMI can't be 100...
                        w_pos = 0
                        c = 0
                        for l in Cycles:
                            if l[2] < weakest[2]:
                                weakest = l
                                w_pos = c
                            c += 1
                        logging.info('      ----> Cycle weakest %s , link PMI %f' % (stringit(weakest), link_value))
                        if weakest[2] < link_value:  # we can eliminate this, because its PMI is smaller than our candidate
                            del Cycles[c - 1]  # we increment always finally
                            logging.info('      ----> link is kept, Cycle weakest %s dropped' % (stringit(weakest)))
                            links = stack + Cycles + [(l, r, link_value)]
                        else:  # even the weakest is stronger than this, so drop link
                            logging.info('       ----> link is not stronger than weakest, link is dropped.')
                            links = stack + Cycles
                    else:  # no cycle, no Xlinks
                        links = stack + [(l, r, link_value)]
                        logging.info ("\nEOL: Links %s + (%d,%d). -> %s " % (stringit(stack), l, r, stringit(links)))

        logging.info ("\n### Finally LINKS:" + stringit(links))

        # we have to tokenize
        final = []
        for l in links:
            final.append(data[ l[0] ], data[l[1]])

        self.tokens.add_data(final)
        return final

        # XXX final question: implement PMI for the Links token





