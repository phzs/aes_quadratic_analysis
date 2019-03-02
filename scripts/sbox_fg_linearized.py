# helper function
def c(o): return F._cache.fetch_int(o)

def f(y):
  return c(0x63) + c(0x05)*y+ c(0x09)*y**2 + c(0xf9)*y**4 + c(0x25)*y**8 + c(0xf4)*y**16 + c(0x01)*y**32 + c(0xb5)*y**64 + c(0x8f)*y**128
