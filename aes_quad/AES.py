from sage.all import *
from key_schedule import AESKeySchedule


"""

Byte Substitution

"""

SBox_M = matrix(GF(2), [
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

pgen = polygen(Integers(2))
modulus = pgen()**8 + pgen()**4 + pgen()**3 + pgen() + 1
gf = FiniteField(2**8, 'a', modulus=modulus)

class AES(SageObject):

    def __init__(self, key=None, rounds=10, block_size=128):
        self.block_size = block_size
        self.key_length = block_size/32 # key length in 32-bit words: AES 128 -> N = 4
        self.rounds = rounds
        self.key_amount = rounds+1

        # initialize key
        if key is not None:
            self.key = []
            missing_bytes = 16
            for i in key:
                self.key.append(gf._cache.fetch_int(ord(i)))
                missing_bytes -= 1
            for i in xrange(missing_bytes):
                self.key.append(gf(0))
            self.key_schedule = AESKeySchedule(self.key, self.key_length, self.key_amount)
        else:
            self.key = None

    def encrypt(self, plaintext):
        state = self.AddRoundKey([gf(0)] * 16, self.key)
        for round in xrange(self.rounds):
            #TODO perform AES round
            print round
        return state

    def decrypt(self, ciphertext):
        pass

    def get_equations(self, known_plaintext, known_ciphertext, **kwargs):
        # key bit variables (8*16 for AES128)
        key_char = 'k'
        key_variable_names = [key_char + str(i) + '_' + str(j)
                              for i in range(self.block_size/8) for j in range(8)]

        """get the polynomial ring over GF(2) with all needed variables
        to represent polynomials with unknown coefficients
        """
        uF = PolynomialRing(GF(2), len(key_variable_names), key_variable_names)
        uF.inject_variables()
        T = PolynomialRing(uF, 'Y')
        Y = T.gen()
        field = T.quotient(Y**8+Y**4+Y**3+Y+1, 'X')

        """build the 16 key polynomials (with unknown coefficients)
        """
        key_coeffs = matrix(16, 8, uF.gens())
        key_polynomials = []
        for i in xrange(16):
            polynomial = field(0)
            for j in xrange(8):
                polynomial += key_coeffs[i][j] * field.gen()**j
            key_polynomials.append(polynomial)
        #key_schedule = AESKeySchedule(key_polynomials, self.key_length, self.key_amount)

    def AddRoundKey(self, state, key):
        return [(state[i] + key[i]) for i in xrange(self.block_size / 8)]

    @staticmethod
    def SubBytes(state):
        def _left_shift(polynomial, shift_by):
            """Performs a circular left shift on a givaro element"""
            new_int_value = int(polynomial._int_repr()) << shift_by
            new_int_value %= (len(gf)-1)
            return gf._cache.fetch_int(new_int_value)
        result = []
        for poly in state:
            if poly is not gf(0):
                inverse = poly ** -1
            else:
                inverse = gf(0)
            sbox_result = inverse + _left_shift(inverse, 1) + _left_shift(inverse, 2) + _left_shift(inverse, 3) + _left_shift(inverse, 4) + gf._cache.fetch_int(0x63)
            result.append(sbox_result)
        return result