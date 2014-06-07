from math import log

def probability(A,Space):
    """Standard probability: freq/Space"""

    return A.freq / Space

def shannon(A,Space):
    """Shannon entropy for the token: -p(A)*log2( p(A) ) 
    If frequency is not set it returns 1.0."""

    if self.freq != 0:
        try:
            # print ('FREQUENCY: ' + str(self.freq) + ' SPACE: ' + str(self.Space))
            p = A.freq / Space
            # print ('Probability: ' + str(p))
            # print ('Shannon: ' + str(-1 * p * log(p, 2)))
            return -1 * p * log(p, 2)
        except:
            raise ValueError('Shannon entropy calculation went wrong')
    else:
        return 1.0


def IC(A,Space):
    """Information content for the token: -log2( p(A) ) 
    If frequency is not set it returns 1.0."""
    if A.freq != 0:
        try:
            # print ('FREQUENCY: ' + str(self.freq) + ' SPACE: ' + str(self.Space))
            p = A.freq / Space
            # print ('Probability: ' + str(p))
            # print ('Shannon: ' + str(-1 * p * log(p, 2)))
            return -1 * log(p, 2)
        except:
            raise ValueError('calculation went wrong')
    else:
        return 1.0

"""Collocation based probabilities"""

def PMI(A, B, Space):
    """Pointwise Mutual Information PMI(A|B) = p(A&B) / p(A)xp(B)"""
    # print ('CO_OCC:' + str(self.co_occurrence))
    co = A.co_occurrence(B)
    if co:
        return log(2, (co * Space) / (A.freq * B.freq))
    else:
        return 0.0
    
def conditional_probability(A, B, Space):
    """Conditional probability on B: p(A&B)/P(B)"""
    if B.idx in A.co_occurrence:
        return A.freq / Space * A[ B.co_occurrence[ B.idx ] ]
    else:
        return 0.0