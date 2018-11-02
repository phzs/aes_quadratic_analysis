#!/usr/bin/env sage

from sage.all import *

R.<x> = PolynomialRing(GF(2), 'x')
S.<y> = QuotientRing(R, R.ideal(x^8+x^4+x^3+x+1))
#assert S.is_field()
#assert S.cardinality() == 256
#assert y^8 + y^4 + y^3 + y + 1 == 0

def generateMixColumn(B):
    return B

print(y^4 + 1)
