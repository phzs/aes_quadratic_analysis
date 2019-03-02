from gf_minimal import F

def S(x_):
  n = lambda a: F._cache.fetch_int(a)
  x = n(x_)
  result = n(0x63)+n(0x8F) *x**127+n(0xB5) *x**191+n(0x01) *x**123+n(0xF4) *x**239+n(0x25) *x**247+n(0xF9) *x**251+n(0x09) *x**253 + n(0x05) *x**254
  return hex(result.integer_representation())
