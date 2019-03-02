#!/usr/bin/env sage

from sage.all import *

var('x y')
V = VectorSpace(GF(2), 8)
eq1 = x+y == 9
eq2 = 2*(x**2)+y == 14
print(solve([eq1, eq2], x, y))
