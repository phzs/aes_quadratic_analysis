from sage.all import *

# block size
block_size = 128
# key length in words
#   AES 128 -> N = 4
key_length = 4
key_amount = 11

pgen = polygen(Integers(2))
modulus = pgen()**8 + pgen()**4 + pgen()**3 + pgen() + 1
F = FiniteField(2**8, 'a', modulus = modulus)
z = F.gen()

# key bit variables (8*16 for AES128)
key_char = 'k'
key_variable_names = [key_char + str(i) + '_' + str(j)
                       for i in range(block_size/8) for j in range(8)]

uF = PolynomialRing(F, len(key_variable_names), key_variable_names)

key_coeffs = matrix(16, 8, uF.gens())
"""
for i in xrange(16):
    polynom = F(0)
    for j in xrange(8):
        key_index = (8*i)+j
#        polynom += F(key_variables[key_index] * (F.gen()**j))
    key_polynomials.append(polynom)
"""

key_polynomials = []
for i in xrange(16):
    polynomial = F(0)
    for j in xrange(8):
        polynomial += key_coeffs[i][j] * F.gen()**j
    key_polynomials.append(polynomial)

print key_polynomials[4]

# rotate a word [a b c d] to [d b c a]
def RotWord(word):
    return vector([word[-1], word[1], word[2], word[3]])

def SubWord(word):
    return vector([S(word[0]), S(word[1]), S(word[2]), S(word[3])])

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
