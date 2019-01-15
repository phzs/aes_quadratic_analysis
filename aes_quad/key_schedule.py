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
        """
        Returns chunks of 4 polynomials in a dictionary with integer keys starting from 0
        :param polyList: list of polynomials
        :return: dictionary of vectors of 4 polynomials for each key
        """
        result = {}
        assert mod(len(polyList), 4) == 0
        index = 0
        for i in xrange(0, len(polyList), 4):
            result[index] = vector(polyList[i:i+4])
            index += 1
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
        """Performs a one-byte left circular shift,
        e.g. [a b c d] to [b c d a]
        :param word: list of elements
        :return: a vector of shifted input list
        """
        return vector([word[1], word[2], word[3], word[0]])

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
                result[i] = result[i-self.key_length] + self.RotWord(self.SubWord(result[i - 1])) + self.rcon(i/self.key_length)
            elif i >= self.key_length and self.key_length > 6 and mod(i, self.key_length) == 4:
                result[i] = result[i-self.key_length] + self.SubWord(result[i-1])
            else:
                result[i] = result[i-self.key_length] + result[i-1]
        return result

    def get_roundkey(self, round):
        index = round * 4
        result = []
        for i in xrange(index,index+4):
            for poly in self.W[i]:
                result.append(poly)
        assert(len(result) == 16)
        return result