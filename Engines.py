from Elements import Atoms, Links
import sys
import logging

logging.basicConfig(stream=sys.stderr, format='%(message)s', level=logging.INFO)

def get_engine(name, elements):
    if name == 'Yuret':
        pass
    raise ValueError(name + 'is not implemented')
import networkx as nx

class Yuret(object):
    """The engine process a given sequence according to the algorithm they represent. Due to the fact that
    the data might be stored in special formats the engine also offers transformation into eg. graph."""

    def __init__(self, atoms):
        self.link_candidates = []
        self.links = Links(atoms)  # we collect the links into an elements list.
        self.sequence = None  # we store the current processed sentence

    def process_sentence(self, data):  # takes a sentence list
        """Takes a list of atoms ( sequence ), creates a link-set and stores as obj.sequence.
        links are: ( l, r, link_value ), where: l - r are positional values in data list, link_value is the calculated pmi."""

        end = len(data)
        links = []
        cycle_pointer = 0
        stringit = lambda x : str(x).strip('[]')
        self.sequence = data

        logging.info('Sentence received : ' + stringit([d.name for d in data]))

        for r in range(1, end):  # take the right element of the link

            right = data[r]
            link_value = -1

            for l in range(r - 1, -1, -1):
                logging.info("L is %d, R is %d" % (l, r))
                link_value = right.PMI(data[l])
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
                            Xlinks = []
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
                        for cLink in Cycles:
                            if cLink[2] < weakest[2]:
                                weakest = cLink
                                w_pos = c
                            c += 1
                        logging.info('      ----> Cycle weakest %s , link PMI %f' % (stringit(weakest), link_value))
                        if weakest[2] < link_value:  # we can eliminate this, because its PMI is smaller than our candidate
                            del Cycles[c - 1]  # we increment always finally
                            logging.info('      ----> link is kept, Cycle weakest %s dropped' % (stringit(weakest)))
                            logging.info ("\nEOL: Links %s + %s + (%d,%d)" % (stringit(stack), stringit(Cycles), l, r,))
                            links = stack + Cycles
                            links.append((l, r, link_value))
                        else:  # even the weakest is stronger than this, so drop link
                            logging.info('       ----> link is not stronger than weakest, link is dropped.')
                            logging.info ("\nEOL: Links %s + %s" % (stringit(stack), stringit(Cycles)))
                            links = stack + Cycles
                    else:  # no cycle, no Xlinks
                        logging.info ("\nEOL: Links %s + (%d,%d)" % (stringit(stack), l, r,))
                        stack.append((l, r, link_value))
                        links = stack


        logging.info ("\n### Finally LINKS:" + stringit(links))

        # we return a list of links object
        final = []
        for l in links:

            link_object = self.links.add_token((data[ l[0] ], data[ l[1] ]))
            final.append(link_object)

        self.sequence = final

    def as_graph(self, graph=None):
        """Creates a graph of the last processed sequence. Returns a networkX graph."""
        # at this level it works but what if we have nested structures?
        # What is a graph if not a set of links? Why do not we put all into a graph?
        if not graph:
            graph = nx.Graph()

        for link in self.sequence:
            logging.info(link)
            (l, r) = link.value
            (ln, rn) = link.name
            logging.info ("Node: %s %s " % (l.name, str(l.shannon)))
            graph.add_node(l.name, shannon=l.shannon, IC=l.IC)
            logging.info ("Node: %s %s " % (r.name, str(r.shannon)))
            graph.add_node(r.name, shannon=r.shannon, IC=r.IC)
            logging.info ("Edge: %s %s %s " % (l.name, r.name, str(link.PMI)))
            graph.add_edge(l.name, r.name, pmi=link.PMI)

        return graph
