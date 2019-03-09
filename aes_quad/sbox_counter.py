from AES import AES

instance = AES(key="123", debug=True, use_key_schedule=True, rounds=1)
instance.encrypt("b"*32)

print "sboxes 1 round 2 block:", AES.sbox_counter

AES.sbox_counter = 0

instance = AES(key="123", debug=False, use_key_schedule=True, rounds=11)
instance.encrypt("b"*32)

print "sboxes 1 round 2 block:", AES.sbox_counter