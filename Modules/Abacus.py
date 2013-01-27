import math

# because it functions over the tokens it should be somehow cleverly incorporated ( I do not mean it is clever )
 
# XXX not necessary maybe
def entropy( name ):
    if name == 'shannon':
        return shannon
    raise ValueError( name + ' is not a defined method' )

def shannon( token ):
    try:
        p = float( token['p'])
        return -1*p*math.log(p,2)
    except: 
        raise ValueError

def probability(states,freq ):
    freq=float(freq)
    return 1/(states/freq)

def attraction( e1, e2 ): # see Yuret: XXX
    s = e1 + e2
    d = e1 - e2
    return s-(e1+d)

# XXX: XXX : TEST
