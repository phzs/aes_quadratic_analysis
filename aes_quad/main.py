#!/usr/bin/env sage
from sage.all import *
from sage.rings.finite_rings.finite_field_givaro import *
from key_schedule import *
import AES

print "-"*13
print "| AES ", AES.block_size, " |"
print "-"*13

rc = AESKeySchedule.generate_rc()
rc_test = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
assert rc.values()[:len(rc_test)] == rc_test # assures that rc begins with rc_test
print "modulus: ", AES.field.modulus()
print "generator:", AES.field.gen()
print "rc\t", rc.values()

schedule = AESKeySchedule(AES.key_polynomials)

print
print "KEY EXPANSION: W"
for i in schedule.W:
    print i, schedule.W[i]
