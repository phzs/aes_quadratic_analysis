from sage.all import *

# block size
block_size = 128
# key length in words
#   AES 128 -> N = 4
key_length = 4
key_amount = 11

var('x a')
key_variables = list(var(" ".join("k%d" % i for i in xrange(8*16))))
F = GF(2**8, 'a') 
F.modulus = a**8 + a**4 + a**3 + a + 1
z = F.gen()

# key bit variables (8*16 for AES128)
key_char = 'k'
key_variable_names = [key_char + str(i) + str(j)
                       for i in range(block_size/8) for j in range(8)]

#uF = PolynomialRing(F, len(key_variable_names), key_variable_names)
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
#        polynom += F(key_variables[key_index] * (F.gen()**j))
    key_polynomials.append(polynom)

# key words
K = []
for i in xrange(128/4):
    K.append(vector(F, key_polynomials[i:i+4]))

# rotate a word [a b c d] to [d b c a]
def RotWord(word):
    return [word[-1], word[1], word[2], word[3]]

def SubWord(word):
    return [S(word[0]), S(word[1]), S(word[2]), S(word[3])]

# affine transformation
SBox_inverseT = matrix(GF(2), [
        [0, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 0]
    ])

def S(polynom):
    #TODO return SBox_M * polynom + SBox_t
    return polynom
