import networkx as nx


def get_attribute(obj, attribute):
    attr = None
    try:
        attr = getattr(obj, attribute)
    except:
        raise AttributeError(str(obj) + ' has no attribute ' + str(attribute))

    return attr


def make_graph_with_attribute(a_graph, sequence, attribute='shannon'):
    """General graph builder method of a given sequence using a given tokenset. The attribute must be a token attribute.
    Returns the modified graph object."""


    prev = ''
    prev_name = ''

    # two possibilities : a list of tokens OR a list of tuples that are already link-elements.

    for token in sequence:

        token_name = token.name

        attr = get_attribute(token, attribute)

        try:
            attr = getattr(token, attribute)
        except:
            print  AttributeError(str(token) + ' has no attribute ' + str(attribute))
            continue

        a_graph.add_node(token_name, pmi=attr)

        if prev:
            try:
                a_graph.edge[prev_name][token_name]
                a_graph.edge[ prev_name ][ token_name ]['weight'] += 1
            except:

                a_graph.add_edge(prev_name, token_name, weight=1, PMI=token.PMI(prev))  # so, we need to add attributes to the link, that is increment the mutual co-occurrence

        prev = token
        prev_name = token.name

    return a_graph


