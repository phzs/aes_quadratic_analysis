from sage.all import mod

from AES import key_length as N
from AES import *

class AESKeySchedule(object):
    def __init__(self):
        self.rc = self.generate_rc() 
        self.W = self.generate_W()

    @staticmethod
    def generate_rc():
        result = {}
        for i in xrange(key_amount):
            if i == 1:
                result[i] = 1
            elif i > 1 and result[i-1] < 0x80:
                result[i] = 2 * result[i-1]
            elif i > 1 and result[i-1] >= 0x80:
                result[i] = (2 * result[i-1]) ^ 0x11B
        return result

    @staticmethod
    def rcon(rc):
        return vector([rc, 0x0, 0x0, 0x0])

    @staticmethod
    def generate_W():
        result = {}
        for i in xrange(key_amount):
            if i < N:
                result[i] = K[i]
            elif i >= N and mod(i, N) == 0:
                result[i] = result[i-N] ^ RotWord(SubWord(result[i-1])) ^ rcon(result[i])
        return result
