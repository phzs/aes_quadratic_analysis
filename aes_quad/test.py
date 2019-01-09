import unittest
from sage.all import vector

from AES import gf, AES
from key_schedule import AESKeySchedule


class TestKeySchedule(unittest.TestCase):

    def test_key_words(self):
        input = [gf._cache.fetch_int(i) for i in xrange(16)]
        expected_result = {0: vector(input[0:4]),
                           1: vector(input[4:8]),
                           2: vector(input[8:12]),
                           3: vector(input[12:16])}
        result = AESKeySchedule.key_words(input)
        self.assertTrue(result == expected_result)


class TestAES(unittest.TestCase):

    def test_AddRoundKey(self):
        instance = AES(key=("test"*3))
        input = [gf._cache.fetch_int(i) for i in xrange(16)]
        key = [gf._cache.fetch_int(i) for i in xrange(16)]
        expected_result = [gf(0)] * 16
        result = instance.AddRoundKey(input, key)
        self.assertTrue(result == expected_result)

        input = [gf._cache.fetch_int(i) for i in xrange(16)]
        key = [gf._cache.fetch_int(i+i) for i in xrange(16)]
        result = instance.AddRoundKey(input, key)
        for i in xrange(len(result)):
            self.assertTrue(result[i] == input[i] + key[i])

    def test_SubBytes(self):
        sbox_input = gf._cache.fetch_int(0x9a)
        expected_result = gf._cache.fetch_int(0xb8)
        result = AES.SubBytes([sbox_input])[0]
        self.assertTrue(result == expected_result)

    def test_SubBytesInv(self):
        sbox_input = gf._cache.fetch_int(0xb8)
        expected_result = gf._cache.fetch_int(0x9a)

        instance = AES()
        result = instance.SubBytesInv([sbox_input])[0]
        self.assertTrue(result == expected_result)

    def test_rc(self):
        rc = AESKeySchedule.generate_rc(11) # generates rc for 11 roundkeys
        rc_test = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
        # assures that rc begins with rc_test
        self.assertTrue(rc.values()[:len(rc_test)] == rc_test)

    def test__left_shift(self):
        input = 0b01000011
        expected_result = 0b00001101
        poly = gf._cache.fetch_int(input)
        result = AES._left_shift(poly, 2)
        self.assertTrue(bin(int(result._int_repr()) == expected_result))

        input = 0b110011
        expected_result = input
        poly = gf._cache.fetch_int(input)
        result = AES._left_shift(poly, 2)
        self.assertTrue(bin(int(result._int_repr()) == expected_result))

if __name__ == '__main__':
        unittest.main()
