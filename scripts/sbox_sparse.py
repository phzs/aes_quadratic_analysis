def S(x):
  return F._cache.fetch_int(0x63) + F._cache.fetch_int(0x8F) *  x^127 + F._cache.fetch_int(0xB5) *  x^191 + F._cache.fetch_int(0x01) *  x^123 + F._cache.fetch_int(0xF4) *  x^239 + F._cache.fetch_int(0x25) *  x^247 + F._cache.fetch_int(0xF9) *  x^251 + F._cache.fetch_int(0x09) *  x^253 + F._cache.fetch_int(0x05) * x^254

def STable(x):
  index = hex(int(x._int_repr()))
  
