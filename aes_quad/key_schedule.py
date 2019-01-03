from sage.all import mod

from AES import key_length as _N
from AES import *

class AESKeySchedule(object):
    def __init__(self, key):
        self.rc = self.generate_rc() 
        self.K = self.key_words(key)
        self.W = self.generate_W(self.K)

    @staticmethod
    def key_words(polyList):
        result = {}
        assert mod(len(polyList), 4) == 0
        for i in xrange((len(polyList)/4)):
            result[i] = vector(polyList[i:i+4])
        return result


    @staticmethod
    def generate_rc():
        result = {}
        for i in xrange(key_amount*4):
            if i == 1:
                result[i] = 1
            elif i > 1 and result[i-1] < 0x80:
                result[i] = 2 * result[i-1]
            elif i > 1 and result[i-1] >= 0x80:
                result[i] = (2 * result[i-1]) ^ 0x11B
        return result

    def rcon(self, i):
        return vector([self.rc[i], 0x0, 0x0, 0x0])

    def generate_W(self, K):
        result = {}
        assert len(K) == _N
        for i in xrange(key_amount*4): # each 128-subkey consists of 4*32bit words
            if i < _N:
                result[i] = K[i]
            elif i >= _N and mod(i, _N) == 0:
                result[i] = result[i-_N] + RotWord(SubWord(result[i-1])) + self.rcon(i)
            elif i >= _N and _N > 6 and mod(i, _N) == 4:
                result[i] = result[i-_N] + SubWord(result[i-1])
            else:
                result[i] = result[i-_N] + result[i-1]
        return result
