import unittest
from sage.all import vector

from AES import gf, AES
from key_schedule import AESKeySchedule

S=[0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
   0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
   0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
   0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
   0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
   0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
   0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
   0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
   0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
   0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
   0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
   0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
   0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
   0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
   0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
   0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16] # rijndael S-box

def test_mask(pos, value=0x91, size=16):
    """
    Helper function which produces a block filled with 0 but only one element != 0 at :pos:
    :param value:
    :param size:
    :param pos: Position where list should have an element != 0
    :return: list with mandatory element at :pos: and gf(0) else (size: 16)
    """
    mask = [gf(0) for i in xrange(size)]
    mask[pos] = gf._cache.fetch_int(value)
    return mask

def string_to_block(string):
    result = []
    for s in string.split(' '):
        hex_value = int(s, 16)
        gf_elem = gf._cache.fetch_int(hex_value)
        result.append(gf_elem)
    return result

class TestKeySchedule(unittest.TestCase):

    def test_key_words(self):
        input = [gf._cache.fetch_int(i) for i in xrange(16)]
        expected_result = {0: vector(input[0:4]),
                           1: vector(input[4:8]),
                           2: vector(input[8:12]),
                           3: vector(input[12:16])}
        result = AESKeySchedule.key_words(input)
        self.assertEquals(expected_result, result)

    def test_generate_rc(self):
        rc = AESKeySchedule.generate_rc(11)
        self.assertEquals([0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36], rc.values())
        for i in xrange(1, 11):
            # each rc can be written as x^(i-1), where i is the round number
            self.assertEquals(int(gf(gf.gen()**(i-1))._int_repr()), rc[i])


    def test_RotWord(self):
        self.assertEquals(vector([1, 2, 3, 0]), AESKeySchedule.RotWord([0, 1, 2, 3]))
        self.assertEquals(vector([0, 0, 0, 10]), AESKeySchedule.RotWord([10, 0, 0, 0]))
        self.assertEquals(vector([1, 1, 1, 1]), AESKeySchedule.RotWord([1, 1, 1, 1]))
        self.assertEquals(vector([5, 3, 6, 7]), AESKeySchedule.RotWord([7, 5, 3, 6]))

    def test_SubWord(self):
        pass

    def test_rcon(self):
        pass

    def test_generate_W(self):
        pass


class TestAES(unittest.TestCase):

    def setUp(self):
        self.gf_full = [i for i in gf]
        self.gf_full.sort()
        self.assertEquals(len(gf), len(self.gf_full))

    def test_AddRoundKey(self):
        # for input = key the result should be 0
        instance = AES(key=("test"*3))
        input = [gf._cache.fetch_int(i) for i in xrange(16)]
        key = [gf._cache.fetch_int(i) for i in xrange(16)]
        expected_result = [gf(0)] * 16
        result = instance.AddRoundKey(input, key)
        self.assertEquals(expected_result, result)

        # for each position the result should be the xor result
        input = [gf._cache.fetch_int(i) for i in xrange(16)]
        key = [gf._cache.fetch_int(i+i) for i in xrange(16)]
        result = instance.AddRoundKey(input, key)
        self.assertEquals(len(result), len(input))
        for i in xrange(len(result)):
            self.assertEquals(input[i] + key[i], result[i])

        # inversion test: applying the same key again should invert the effect
        input = [gf._cache.fetch_int(2*i) for i in xrange(16)]
        key = [gf._cache.fetch_int(i**2) for i in xrange(16)]
        result = instance.AddRoundKey(input, key)
        self.assertEquals(input, instance.AddRoundKey(result, key))

    def test_SubBytes(self):
        sbox_input = gf._cache.fetch_int(0x9a)
        expected_result = gf._cache.fetch_int(0xb8)
        result = AES.SubBytes([sbox_input])[0]
        self.assertEquals(expected_result, result)

    def test_SubBytesInv(self):

        # test single substitution
        sbox_input = gf._cache.fetch_int(0xb8)
        expected_result = gf._cache.fetch_int(0x9a)

        instance = AES()
        result = instance.SubBytesInv([sbox_input])[0]
        self.assertEquals(expected_result, result)

        poly = gf._cache.fetch_int(0x99)
        self.assertEquals(poly, instance.SubBytesInv(instance.SubBytes([poly]))[0])

        # full inversion test
        self.assertEquals(self.gf_full, instance.SubBytesInv(instance.SubBytes(self.gf_full)))

    def test_SubBytes_table(self):
        result = AES.SubBytes(self.gf_full)

        for (i, expected_int) in enumerate(S):
            self.assertEquals(expected_int, int(result[i]._int_repr()))

    def test_SubBytesInv_table(self):
        input = [gf._cache.fetch_int(i) for i in S]
        assert input[125] == gf._cache.fetch_int(255)
        result = AES().SubBytesInv(input)

        for (i, expected_gfe) in enumerate(result):
            expected_int = int(expected_gfe._int_repr())
            if expected_int is not i:
                print expected_int, i
            self.assertEquals(expected_int, i)

    def test_ShiftRowsInv(self):
        instance = AES()
        test_indice_replacement = [(0, 0), (8, 8), (4, 4), (12, 12),
                                   (1, 13), (5, 1), (9, 5), (13, 9),
                                   (2, 10), (6, 14), (10, 2), (14, 6),
                                   (3, 7), (7, 11), (11, 15), (15, 3)]

        for indices in test_indice_replacement:
            self.assertEquals(test_mask(indices[1]), instance.ShiftRowsInv(test_mask(indices[0])),
                              msg="indice %d is not replaced correctly" % indices[0])

        # full inversion test
        for block in instance._get_blocks(self.gf_full):
            test_input = block
            self.assertEquals(test_input, instance.ShiftRowsInv(instance.ShiftRows(test_input)))
            self.assertNotEqual(test_input, instance.ShiftRowsInv(test_input))

    def test_MixColumnsInv(self):
        instance = AES()

        # full inversion test
        for i in xrange(0, len(self.gf_full), 16):
            test_input = self.gf_full[i:i+16]
            self.assertEquals(test_input, instance.MixColumnsInv(instance.MixColumns(test_input)))
            self.assertNotEqual(test_input, instance.MixColumnsInv(test_input))

    def test_rc(self):
        rc = AESKeySchedule.generate_rc(11) # generates rc for 11 roundkeys
        rc_test = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
        # assures that rc begins with rc_test
        self.assertEquals(rc_test, rc.values()[:len(rc_test)])

    def test__left_shift(self):
        input = 0b01000011
        expected_result = 0b00001101
        poly = gf._cache.fetch_int(input)
        result = AES._left_shift(poly, 2)
        self.assertEquals(expected_result, int(result._int_repr()))

        input = 0b00110011
        expected_result = 0b11001100
        poly = gf._cache.fetch_int(input)
        result = AES._left_shift(poly, 2)
        self.assertEquals(expected_result, int(result._int_repr()))

        input = 0b11111111
        expected_result = 0b0
        poly = gf._cache.fetch_int(input)
        result = AES._left_shift(poly, 2)
        self.assertEquals(expected_result, int(result._int_repr()))

        input = 0b0
        expected_result = input
        poly = gf._cache.fetch_int(input)
        result = AES._left_shift(poly, 2)
        self.assertEquals(expected_result, int(result._int_repr()))

    def test_encrypt_decrypt(self):
        instance = AES(key="sometestkey", rounds=11)

        plaintext = "some message to encrypt"
        ciphertext = instance.encrypt(plaintext)
        decrypted_plaintext = instance.decrypt(ciphertext)
        self.assertEquals(plaintext, AES.state_str(decrypted_plaintext))

if __name__ == '__main__':
        unittest.main()
