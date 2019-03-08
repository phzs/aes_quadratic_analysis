#!/usr/bin/env sage
from sage.all import *
from AES import AES
from EquationSystem import EquationSystem

import time

key = "sometestkey"
instance = AES(key=key, rounds=1)

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

print
print "equations"
print "-"*80
start = time.time()
eqs = instance.get_equations(plaintext, ciphertext)
end = time.time()
print "-"*80
print "equations generated in %d seconds" % (end-start)
#for i, equation in enumerate(eqs.get_equations()):
#    print i, equation

#print "solution", "-"*20
#print "gens:", eqs.base.gens()
#print eqs.solve()

print "inserting the key:", key
print "-"*80
start = time.time()
all_true = True
not_true = 0
for eq in eqs.substitute_key(key):
    if not bool(eq):
        print eq, bool(eq)
        all_true = False
        not_true += 1
print "all true: ", all_true
print "not true: %d/%d" % (not_true, len(eqs.get_equations()))

end = time.time()
print "-"*80
print "substitution finished in %d seconds" % (end-start)