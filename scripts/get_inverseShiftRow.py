from sage.all import *

M = MatrixSpace(QQ,4,4)

def f(m):
    return matrix([
            [m[0][0], m[0][1], m[0][2], m[0][3]],
            [m[1][3], m[1][0], m[1][1], m[1][2]],
            [m[2][2], m[2][3], m[2][0], m[2][1]],
            [m[3][1], m[3][2], m[3][3], m[3][0]]
        ])
for b in M.basis():
    print f(b)
    print "-"*20

print linear_transformation(M,M,f)
