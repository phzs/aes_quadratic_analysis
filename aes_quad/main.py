#!/usr/bin/env sage
from sage.all import *
from AES import AES

instance = AES(key="test", rounds=2, block_size=128)

plaintext = "some message to encrypt"
print "plaintext", len(plaintext)
ciphertext = instance.encrypt(plaintext)

print plaintext, "->", " ".join([str(hex(int(c._int_repr())))[2:] for c in ciphertext])
print "<-", "".join([chr(int(c._int_repr())) for c in instance.decrypt(ciphertext)])