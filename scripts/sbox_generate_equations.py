# coding: utf-8
"""
pgen = polygen(Integers(Integer(2)))
modulus = pgen()**Integer(8) + pgen()**Integer(4) + pgen()**Integer(3) + pgen() + Integer(1)
F = FiniteField(Integer(2)**Integer(8), 'X', modulus = modulus)
z = F.gen()

x_coeffs = list(var('x_%d' % i) for i in range(Integer(8)))
y_coeffs = list(var('y_%d' % i) for i in range(Integer(8)))
uF = PolynomialRing(F, Integer(16), x_coeffs + y_coeffs)

poly_x = uF(x_0 * X**Integer(0) + x_1 * X**Integer(1) + x_2 * X**Integer(2) + x_3 * X**Integer(3) + x_4 * X**Integer(4) + x_5 * X**Integer(5) + x_6 * X**Integer(6) + x_7 * X**Integer(7))
poly_y = uF(y_0 * X**Integer(0) + y_1 * X**Integer(1) + y_2 * X**Integer(2) + y_3 * X**Integer(3) + y_4 * X**Integer(4) + y_5 * X**Integer(5) + y_6 * X**Integer(6) + y_7 * X**Integer(7))

"""

S = PolynomialRing(GF(2), names=['x_{}'.format(d) for d in range(8)] + ['y_{}'.format(d) for d in range(8)])
S.inject_variables()
T.<Y> = PolynomialRing(S)
U.<X> = T.quotient(Y^8+Y^4+Y^3+Y+1)
x = x_0 + x_1*X + x_2*X^2 + x_3*X^3 + x_4*X^4 + x_5*X^5 + x_6*X^6 + x_7*X^7
y = y_0 + y_1*X + y_2*X^2 + y_3*X^3 + y_4*X^4 + y_5*X^5 + y_6*X^6 + y_7*X^7

# (x * y).list():
print x * y
