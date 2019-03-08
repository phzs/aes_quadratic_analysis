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
def var_names(var):
   return [var+'_{}'.format(d) for d in range(8)]
S = PolynomialRing(GF(2), names=var_names('x') + var_names('y') + var_names('z'))
S.inject_variables()
T.<Y> = PolynomialRing(S)
U.<X> = T.quotient(Y^8+Y^4+Y^3+Y+1)
x = x_0 + x_1*X + x_2*X^2 + x_3*X^3 + x_4*X^4 + x_5*X^5 + x_6*X^6 + x_7*X^7
y = y_0 + y_1*X + y_2*X^2 + y_3*X^3 + y_4*X^4 + y_5*X^5 + y_6*X^6 + y_7*X^7
z = z_0 + z_1*X + z_2*X^2 + z_3*X^3 + z_4*X^4 + z_5*X^5 + z_6*X^6 + z_7*X^7

# Rechte Seite der Gleichungen für 1 = xy
print reversed((x * y).list())

gf = GF(2^8)
gf.modulus = X^8 + X^4 + X^3 + 1

SBox_M = matrix(GF(2), [
    [1, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 1]
])

SBox_t = vector(GF(2), [1, 1, 0, 0, 0, 1, 1, 0])

# Hexadezimalwert für t
hex(gf(SBox_t).integer_representation()) # 0x63

hex(gf(SBox_M^-1 * SBox_t).integer_representation()) # 0x05

# Berechnen der Koeffizienten von y in Abhängigkeit von z nach der Formel
# y = M^-1 * z + 0x05
y_ = SBox_M^-1 * vector(z) + vector(gf._cache.fetch_int(0x05))

# Einsetzen von y_ in die rechte Seite der Gleichung 1 = xy
eqs_right = []
for right in reversed((x*y).list()):
    eqs_right.append(right.subs(y_0=y_[0],y_1=y_[1],y_2=y_[2],
                     y_3=y_[3],y_4=y_[4],y_5=y_[5],y_6=y_[6],y_7=y_[7]))
    print eqs_right

# Hilfsfunktionen zum Erweitern des Gleichungssystems

def substitute_y(polynomial, y_):
    return polynomial.subs(y_0=y_[0],y_1=y_[1],y_2=y_[2],
                           y_3=y_[3],y_4=y_[4],y_5=y_[5],y_6=y_[6],y_7=y_[7])

def generate_equations(generator):
    equations = []
    for right in reversed(generator.list()):
        equations.append(substitute_y(right, y_))
    return equations

# Erweitern des Gleichungssystems: