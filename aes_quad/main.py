#!/usr/bin/env sage
from sage.all import *
from sage.rings.finite_rings.finite_field_givaro import *
from key_schedule import *
import AES

print "-"*13
print "| AES ", AES.block_size, " |"
print "-"*13
print "modulus: ", AES.field.modulus()
print "generator:", AES.field.gen()

schedule = AESKeySchedule(AES.key_polynomials)

print
print "KEY EXPANSION: W"
#    print i, len(schedule.W[i])
