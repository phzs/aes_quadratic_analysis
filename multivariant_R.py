#!/usr/bin/env sage

from sage.all import *

var('x y z')
eq1 = x+y == 9
eq2 = 2*(x**2)+y == 14
output = latex(solve([eq1, eq2], x, y))
print output
