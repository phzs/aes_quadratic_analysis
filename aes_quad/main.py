#!/usr/bin/env sage
from sage.all import *
from sage.rings.finite_rings.finite_field_givaro import *
from key_schedule import *
import AES

#k.<a> = GF(2^8)
print "AES", AES.block_size
print "modulus: ", AES.k.modulus()
print "generator:", AES.k.gen()

rc_test = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
print "rc_test\t", rc_test
print "rc\t", AESKeySchedule.generate_rc().values()

schedule = AESKeySchedule()
print schedule.W

print AES.polynom(0x37)
