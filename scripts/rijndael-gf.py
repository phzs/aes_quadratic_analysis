from sage.all import *
from sage.crypto.mq.rijndael_gf import RijndaelGF

# block size: 4, key size: 6
rgf = RijndaelGF(4, 6)

plaintext = '00112233445566778899aabbccddeeff'
key = '000102030405060708090a0b0c0d0e0f1011121314151617'

ciphertext = rgf.encrypt(plaintext, key) 
print "encryption works: ", rgf(ciphertext, key, algorithm='decrypt') ==  plaintext
print
print "SHIFT ROWS"
print rgf.shift_rows_poly_constr()(1, 2, algorithm='decrypt')
print
print "MIX COLUMNS"
print rgf.mix_columns_poly_constr()(1, 2, algorithm='decrypt')
print
print "SUBSTITUTION BYTES (no inversions)"
print rgf.sub_bytes_poly_constr()(1, 2, algorithm='decrypt', no_inversion=True)
print
print "STATE"
print rgf.state_vrs

import pdb; pdb.set_trace()