import unittest

from AES import *
from key_schedule import AESKeySchedule

class TestAES(unittest.TestCase):

    def test_SBox(self):
        sbox_input = F._cache.fetch_int(0x9a)
        print "sbox_input", sbox_input
        expected_result = F._cache.fetch_int(0xb8)
        print "expected_result", expected_result
        result = S(sbox_input) 
        print "result", result
        self.assertTrue(result == expected_result)

    def test_rc(self):
        rc = AESKeySchedule.generate_rc()
        rc_test = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
        # assures that rc begins with rc_test
        self.assertTrue(rc.values()[:len(rc_test)] == rc_test)

if __name__ == '__main__':
        unittest.main()
