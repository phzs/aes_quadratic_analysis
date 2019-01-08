import unittest

from AES import gf, AES
from key_schedule import AESKeySchedule

class TestAES(unittest.TestCase):

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

if __name__ == '__main__':
        unittest.main()
