from sage.all import mod, vector

class AESKeySchedule(object):

    def __init__(self, key, key_length, key_amount):
        self.key_length = key_length
        self.key_amount = key_amount
        self.rc = self.generate_rc(self.key_amount)
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
    def generate_rc(key_amount):
        result = {}
        for i in xrange(key_amount*4):
            if i == 1:
                result[i] = 1
            elif i > 1 and result[i-1] < 0x80:
                result[i] = 2 * result[i-1]
            elif i > 1 and result[i-1] >= 0x80:
                result[i] = (2 * result[i-1]) ^ 0x11B
        return result


    @staticmethod
    def RotWord(word):
        """rotates a word [a b c d] to [d b c a]"""
        return vector([word[-1], word[1], word[2], word[3]])

    @staticmethod
    def SubWord(word):
        from AES import AES
        temp = AES.SubBytes(word)
        return vector(temp)

    def rcon(self, i):
        return vector([self.rc[i], 0x0, 0x0, 0x0])

    def generate_W(self, K):
        result = {}
        assert len(K) == self.key_length
        for i in xrange(self.key_amount*4): # each 128-subkey consists of 4*32bit words
            if i < self.key_length:
                result[i] = K[i]
            elif i >= self.key_length and mod(i, self.key_length) == 0:
                result[i] = result[i-self.key_length] + self.RotWord(self.SubWord(result[i - 1])) + self.rcon(i)
            elif i >= self.key_length and self.key_length > 6 and mod(i, self.key_length) == 4:
                result[i] = result[i-self.key_length] + self.SubWord(result[i-1])
            else:
                result[i] = result[i-self.key_length] + result[i-1]
        return result

    def get_roundkey(self, round):
        index = round * 4
        return self.W[index:index+4]