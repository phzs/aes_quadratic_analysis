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

print key_polynomials[4]

# rotate a word [a b c d] to [d b c a]
def RotWord(word):
    return vector([word[-1], word[1], word[2], word[3]])

def SubWord(word):
    return vector([S(word[0]), S(word[1]), S(word[2]), S(word[3])])

"""

Byte Substitution

"""

SBox_M = matrix(uF, [
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1]
    ])

SBox_t = vector(GF(2), [1, 1, 0, 0, 0, 1, 1, 0])

SBox_inverse_M = matrix(GF(2), [
        [0, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 0]
    ])

SBox_inverse_t = vector(GF(2), [1, 0, 1, 0, 0, 0, 0, 0])

def reverse(input_vector):
    tmp = input_vector.list()
    tmp.reverse()
    return(vector(tmp))

# builds a polynomial over `parent` which has the coefficients listed in `input_vector`
# the vector must start with the coefficient of the highest grade (high to low)
def polynomial_from_vector(parent, input_vector):
    result = parent(0)
    for (i, coeff) in enumerate(reverse(input_vector)):
        result += parent(coeff * parent.gen()**i)
    return result

def S(polynomial):
    #F(SBox_M * vector(vector(uF, polynom)[1::2]) + SBox_t)
    # calculate the inverse
    #polynomial = polynomial**(256-2)

    # vector(uF, polynom) is a vector of both coefficients and generators
    #   [1::2] ([start:stop:step]) selects only coefficients
    if type(polynomial) == sage.rings.polynomial.multi_polynomial_libsingular.MPolynomial_libsingular:
        coeffs = vector(uF, polynomial)[1::2]
        #elif type(polynomial) == sage.rings.finite_rings.element_givaro.FiniteField_givaroElement:
        #    coeffs = vector(polynom)

        # M * v (calculate coefficients only)
        mult_result = [sum([SBox_M[i][j]*coeffs[j] for j in xrange(len(SBox_M.columns()))]) 
                for i in xrange(len(SBox_M.rows()))]

        # insert variables again
        coeff_vector = vector([uF(mult_result[i]) for i in xrange(len(mult_result))])
        mult_result = coeff_vector * F(vector(GF(2), [1]*8)) # ?

        # add the vector
        result = mult_result + SBox_t
    else:
        coeffs = vector(polynomial)
        #coeffs = reverse(coeffs)

        mult_result = SBox_M * coeffs
        
        add_result = mult_result + SBox_t

        result = polynomial_from_vector(polynomial.parent(), add_result)   

    return result
