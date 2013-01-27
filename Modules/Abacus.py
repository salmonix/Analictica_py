import math
from numpy import array, zeros
from copy import copy

# because it functions over the tokens it should be somehow cleverly incorporated ( I do not mean it is clever )
 
# XXX not necessary maybe
def entropy( name ):
    if name == 'shannon':
        return shannon
    raise ValueError( name + ' is not a defined method' )

def shannon( token ):
    try:
        p = float( token['p'] )
        return -1*p*math.log(p,2)
    except: 
        raise ValueError

def probability(states,freq ):
    freq=float(freq)
    return 1/(states/freq)

# this is an abnomination, simply it repeats itself. The half of the table is enough but 
# I have no brain for that, plus it is a bit simpler in the joined_probability_table now...
def co_occurrence_table( elements, on_value='freq' ):
    """Builds a token x token table showing the frequency of co-occurrence in one sentence. Returns a table."""
    tokens = elements.tokens
    texts = elements.texts
    dim = tokens.idx+1
    table = zeros( (dim, dim ) )
    sentences = texts.get_sentences()
    for s in sentences:
        print (s)
        for r in range( 0, len(s)):
            for c in range( r+1, len(s)):
#                print (str(s[r])+':'+str(s[c]))
                x = s[r]
                y = s[c]
                if y != x:
                    table[x][y] += 1
                    table[y][x] += 1
    return table

# P(A|B) = table[A][B]
def joined_probability_table( table, tokens ):
    p_table = copy(table)
    dim = len(p_table)
    print ( 'co-occurrence:')
    print table
    for y in range(0, dim ): # ROWS
        freq = tokens.tokens[y]['freq']
        for x in range( 0, dim ): # B columns
            if table[x][y] > 0:
                p = freq/table[x][y]
                p_table[x][y]=p
                print ( str(x) + ':' + str(y) + ' -> ' + str( table[x][y] ) + '/' + str(freq) + '->' + str(p) )

    print "\nj_probab:"
    print p_table
    return p_table

# NO SANITY CHECK !!
def mutual_gain_table( j_probab, tokens ):
    m_g_table = copy( j_probab )
    dim = len(j_probab)
    for y in range(0, dim ): # ROWS
        freq = tokens.tokens[y]['freq']
        for x in range( 0, dim ): # B columns
            if j_probab[x][y] != 0:  # perhaps it should be 1? Because A is  always with A
                p = j_probab[x][y]/tokens.tokens[y]['p']*tokens.tokens[x]['p'] 
                print ( str(x) + ':'+str(y) + ' -> ' + str( j_probab[x][y] ) + ' / ' + str ( tokens.tokens[y]['p'] ) + '*' + str(tokens.tokens[x]['p']) + ' = ' + str(p))
                if p != 1.0:
                    gain = -1*math.log(2,p )
                else:
                    m_g_table[x][y] = gain

    print "\n"
    print m_g_table

    return m_g_table

# XXX: XXX : TEST
