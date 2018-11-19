#!/usr/bin/env sage
from sage.all import *
from sage.rings.finite_rings.finite_field_givaro import *
from key_schedule import *
import AES

print "-"*13
print "| AES ", AES.block_size, " |"
print "-"*13
print "modulus: ", AES.F.modulus()
print "generator:", AES.F.gen()

rc = AESKeySchedule.generate_rc()
rc_test = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
assert rc_test == rc.values()
print "rc\t", rc.values()

schedule = AESKeySchedule()


print
print "KEY EXPANSION: W"
for subkey_index in schedule.W:
    print subkey_index, schedule.W[subkey_index]
