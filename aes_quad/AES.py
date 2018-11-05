from sage.all import *

# block size
block_size = 128
# key length in words
#   AES 128 -> N = 4
key_length = 4
key_amount = 11

var('x a')
key_variables = list(var(" ".join("k%d" % i for i in xrange(8*16))))
#k = GF(2**8, x, modulus)
P = PolynomialRing(GF(2), 128+1, [x]+key_variables) # to enforce modulo comp.
modulus = x**8 + x**4 + x**3 + x + 1
F = GF(2**8, a, modulus)

# key bit variables (8*16 for AES128)
#var('k0 k1 k2 k3 k4 k5 k6 k7 k8 k9 k10 k11 k12 k13 k14 k15')

# list of key variables: key_length 32bit-vectors
"""
K = [
        vector([k0, k1, k2, k3]),
        vector([k4, k5, k6, k7]),
        vector([k8, k9, k10, k11]), 
        vector([k12, k13, k14, k15])
    ]
"""

key_polynomials = []
for i in xrange(16):
    polynom = F(0)
    for j in xrange(8):
        key_index = (8*i)+j
        polynom += F(P.gen(key_index+1) * (F.gen()**j))
    key_polynomials.append(polynom)

# key words
K = []
for i in xrange(N):
    K.append(vector(F, key_polynomials[i:i+4]))

# kann ersetzt werden mit k._cache.fetch_int(...)
def polynom(numerical_repr):
    result = k(0) # null polynom
    print "init", result
    for i in xrange(8):
        coeff = int((numerical_repr & (1 << i)) != 0)
        subpoly =  k(coeff * (k.gen()**i))
        result += subpoly
    return result

# rotate a word [a b c d] to [d b c a]
def RotWord(word):
    return [word[-1], word[1], word[2], word[3]]

def SubWord(word):
    return [S(word[0]), S(word[1]), S(word[2]), S(word[3])]

# affine transformation
SBox_inverseT = matrix(F, [
        [0, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 0]
    ])
print SBox_inverseT

def S(polynom):

    #TODO calculate multiplicative inverse
    return polynom #TODO
