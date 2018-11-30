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

key_polynomials = []
for i in xrange(16):
    polynomial = F(0)
    for j in xrange(8):
        polynomial += key_coeffs[i][j] * F.gen()**j
    key_polynomials.append(polynomial)

