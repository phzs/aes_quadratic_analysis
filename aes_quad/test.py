import unittest

from AES import *

class TestAES(unittest.TestCase):

    def test_SBox(self):
        sbox_input = F._cache.fetch_int(0x9a)
        print "sbox_input", sbox_input
        expected_result = F._cache.fetch_int(0xb8)
        print "expected_result", expected_result
        result = S(sbox_input) 
        print "result", result
        self.assertTrue(result == expected_result)


if __name__ == '__main__':
        unittest.main()
