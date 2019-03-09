from AES import AES

instance = AES(key="123", debug=True, use_key_schedule=True, rounds=1)
instance.encrypt("blub")

print "sboxes:", AES.sbox_counter