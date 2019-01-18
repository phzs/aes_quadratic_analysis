#!/usr/bin/env sage
from sage.all import *
from AES import AES

instance = AES(key="sometestkey", rounds=2)

plaintext = "some message to encrypt"
print "plaintext:", plaintext
print "plaintext length:", len(plaintext)
ciphertext = instance.encrypt(plaintext)

print "ENCRYPTION RESULT"
print plaintext, "->", AES.state_int(ciphertext)
print
print "DECRYPTION RESULT"
decrypted_plaintext = instance.decrypt(ciphertext)
print AES.state_int(ciphertext), "->", AES.state_str(decrypted_plaintext)

