#!/usr/bin/env sage
from sage.all import *
from AES import AES

instance = AES(key="test", rounds=1, block_size=128)

plaintext = "some message"
ciphertext = instance.encrypt(plaintext)
#assert instance.decrypt(ciphertext) is plaintext

print instance.get_equations(ciphertext, plaintext, rounds=1)