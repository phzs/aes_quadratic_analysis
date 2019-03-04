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
    return vector(tmp)

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

mix_columns_M = matrix(gf, [
    [gf._cache.fetch_int(0x02), gf._cache.fetch_int(0x03), gf._cache.fetch_int(0x01), gf._cache.fetch_int(01)],
    [gf._cache.fetch_int(0x01), gf._cache.fetch_int(0x02), gf._cache.fetch_int(0x03), gf._cache.fetch_int(01)],
    [gf._cache.fetch_int(0x01), gf._cache.fetch_int(0x01), gf._cache.fetch_int(0x02), gf._cache.fetch_int(03)],
    [gf._cache.fetch_int(0x03), gf._cache.fetch_int(0x01), gf._cache.fetch_int(0x01), gf._cache.fetch_int(02)],
])

mix_columns_inverse_M = matrix(gf, [
    [gf._cache.fetch_int(0x0E), gf._cache.fetch_int(0x0B), gf._cache.fetch_int(0x0D), gf._cache.fetch_int(0x09)],
    [gf._cache.fetch_int(0x09), gf._cache.fetch_int(0x0E), gf._cache.fetch_int(0x0B), gf._cache.fetch_int(0x0D)],
    [gf._cache.fetch_int(0x0D), gf._cache.fetch_int(0x09), gf._cache.fetch_int(0x0E), gf._cache.fetch_int(0x0B)],
    [gf._cache.fetch_int(0x0B), gf._cache.fetch_int(0x0D), gf._cache.fetch_int(0x09), gf._cache.fetch_int(0x0E)],
])

class AES(SageObject):

    def __init__(self, key=None, rounds=10, block_size=128, debug=False):
        self.block_size = block_size
        self.key_length = block_size/32 # key length in 32-bit words: AES 128 -> N = 4
        self.rounds = rounds
        self.key_amount = rounds+1
        self.print_debug_output = debug

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
        result = []
        self.debug("ENCRYPT")
        self.debug("-"*40)
        for block in self._get_blocks(plaintext, " "):
            self.debug("BLOCK")
            converted_block = [gf._cache.fetch_int(ord(entry)) for entry in block]
            self.debug_state("  \t", converted_block)
            _main_key = self.key_schedule.get_roundkey(0)
            state = self.AddRoundKey(converted_block, _main_key)
            self.debug_state("   AddRK %d" % 0, state, key=_main_key)
            for round_num in xrange(self.rounds):

                state = self.SubBytes(state)
                self.debug_state("%d  SubBytes" % round_num, state)

                state = self.ShiftRows(state)
                self.debug_state("%d  ShiftRows" % round_num, state)

                if round_num is not (self.rounds-1):
                    state = self.MixColumns(state)
                    self.debug_state("%d  MixColumns" % round_num, state)

                _round_key = self.key_schedule.get_roundkey(round_num+1)
                state = self.AddRoundKey(state, _round_key)
                self.debug_state("%d  AddRK %d" % (round_num, round_num+1), state, key=_round_key)
            result += state
        return result

    def decrypt(self, ciphertext):
        result = []
        for symbol in ciphertext:
            assert(isinstance(symbol, sage.rings.finite_rings.element_givaro.FiniteField_givaroElement))
        for block in self._get_blocks(ciphertext, " "):
            self.debug("BLOCK")
            self.debug_state("  \t", block)
            state = block
            for round_num in reversed(xrange(self.rounds)):

                _round_key = self.key_schedule.get_roundkey(round_num+1)
                state = self.AddRoundKey(state, _round_key)
                self.debug_state("%d  AddRK %d" % (round_num, round_num+1), state, key=_round_key)

                if round_num is not (self.rounds-1):
                    state = self.MixColumnsInv(state)
                    self.debug_state("%d  MixCInv" % round_num, state)

                state = self.ShiftRowsInv(state)
                self.debug_state("%d  ShiftRInv" % round_num, state)

                state = self.SubBytesInv(state)
                self.debug_state("%d  SubBInv" % round_num, state)

            _main_key = self.key_schedule.get_roundkey(0)
            state = self.AddRoundKey(state, _main_key)
            self.debug_state("   AddRK %d" % 0, state, key=_main_key)
            result += state
        return result

    def get_equations(self, known_plaintext, known_ciphertext):
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
        return [(state[i] + key[i]) for i in xrange(len(state))]

    def ShiftRows(self, state):
        result = [gf(0) for i in xrange(16)]
        result[0] = state[0]
        result[4] = state[4]
        result[8] = state[8]
        result[12] = state[12]
        result[5] = state[1]
        result[9] = state[5]
        result[13] = state[9]
        result[1] = state[13]
        result[10] = state[2]
        result[14] = state[6]
        result[2] = state[10]
        result[6] = state[14]
        result[15] = state[3]
        result[3] = state[7]
        result[7] = state[11]
        result[11] = state[15]

        return result

    def ShiftRowsInv(self, state):
        result = [gf(0) for i in xrange(16)]
        result[0] = state[0]
        result[8] = state[8]
        result[4] = state[4]
        result[12] = state[12]
        result[13] = state[1]
        result[1] = state[5]
        result[5] = state[9]
        result[9] = state[13]
        result[10] = state[2]
        result[14] = state[6]
        result[2] = state[10]
        result[6] = state[14]
        result[7] = state[3]
        result[11] = state[7]
        result[15] = state[11]
        result[3] = state[15]

        return result

    def MixColumns(self, state):
        return self._MixColumns(state, mix_columns_M)

    def MixColumnsInv(self, state):
        return self._MixColumns(state, mix_columns_inverse_M)

    def _MixColumns(self, state, matrix):
        result = []
        for i in xrange(0, self.block_size/8, 4):
            """multiply the mix columns matrix with each vector of 4 polynomials;
            concatenate the result"""
            result += list(matrix * vector(state[i:i+4]))
        return result

    def _get_blocks(self, sequence, fill_value=None):
        """
        Returns iterable of blocks of size :self.block_size:, fills up with :fillvalue:
        :param sequence: list of values
        :param fill_value: value to fill in gaps (padding)
        :return: list of blocks of size :self.block_size:
        """
        values = list(sequence)
        size = self.block_size / 8
        while (len(values) % size) is not 0:
            values.append(fill_value)

        return (values[pos:pos + size] for pos in xrange(0, len(values), size))

    @staticmethod
    def _left_shift(polynomial, shift_by):
        """Performs a circular left shift on a givaro element"""
        new_int_value = int(polynomial._int_repr()) << shift_by
        new_int_value %= (len(gf)-1)
        return gf._cache.fetch_int(new_int_value)

    @staticmethod
    def SubBytes(state):
        result = []
        for poly in state:
            if poly is not gf(0):
                inverse = poly ** -1
            else:
                inverse = gf(0)
            sbox_result = inverse + AES._left_shift(inverse, 1) \
                          + AES._left_shift(inverse, 2) \
                          + AES._left_shift(inverse, 3) \
                          + AES._left_shift(inverse, 4) + gf._cache.fetch_int(0x63)
            result.append(sbox_result)
        return result

    def SubBytesInv(self, state):
        result = []
        for poly in state:
            # calculate the inverse affine transformation first
            if poly is gf._cache.fetch_int(255):
                # workaround for the special case x = 0
                result.append(gf._cache.fetch_int(0x7d))
                continue
            trans_result = self._left_shift(poly, 1) \
                   + self._left_shift(poly, 3) \
                   + self._left_shift(poly, 6) + gf._cache.fetch_int(0x05)
            if trans_result is not gf(0):
                sbox_result = trans_result ** -1
            else:
                sbox_result = gf(0)
            result.append(sbox_result)
        return result

    @staticmethod
    def state_int(state):
        """
        Converts a AES state into a sequence of readable numbers (base 16)
        :param state: AES state consisting of givaro elements
        :return: string representing the state as a sequence of numbers (base 16)
        """
        return " ".join([str("{:0>2x}".format(int(symbol._int_repr()))) for symbol in state])

    @staticmethod
    def state_str(state):
        """
        Converts a AES state into a string
        :param state: AES state consisting of givaro elements
        :return: string
        """
        def filter(char):
            escape = False
            if char in ('\n', '\r'):
                escape = True
            return '\%s' % char if escape else char
        return r"".join([filter(chr(int(symbol._int_repr()))) for symbol in state]).strip()

    def debug_state(self, description, state, **kwargs):
        if self.print_debug_output:
            _key = ""
            if 'key' in kwargs:
                _key = AES.state_int(kwargs['key'])
            print description, "\t", AES.state_int(state), "\t", _key

    def debug(self, message):
        if self.print_debug_output:
            print message
