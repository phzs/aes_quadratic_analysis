from sage.all import solve, vector, var

from AES import AES
from key_substitution import substitute_key_vars


class EquationSystem():
    def __init__(self, base, field):
        self.base = base
        self.field = field
        self.equations = []

    def set_equations(self, equations):
        self.equations = equations

    def get_equations(self):
        return self.equations

    def substitute_key(self, key):
        result = []
        self.base.inject_variables(verbose=False)
        key_bytes = AES.convert_key(key)

        substitutions = {}
        print "generating substitutions"
        for (i, g) in enumerate(self.base.gens()):
            polynomial_number = i % 16
            coefficient_number = i % 8
            key_bit = [x for x in reversed(vector(key_bytes[polynomial_number]))][coefficient_number]
            var('uu')
            substitutions[g] = key_bit

        print "substitution in progress"

        for equation in self.equations:
            subs_equation = substitute_key_vars(equation, substitutions, self.base)

            result.append(subs_equation)
        return result

    def solve(self):
        # first make sure that one side of each equation is zero
        equations_zero = []
        for equation in self.equations:
            if equation.left() is self.base(0):
                equations_zero.append(equation.right())
            elif equation.right() is self.base(0):
                equations_zero.append(equation.left())
            else:
                equations_zero.append(equation.left() - equation.right())
        I = self.field.ideal(equations_zero)
        if I.dimension() is not 0:
            raise ValueError("Dimension of ideal is not zero. No solution found.")
        return I.variety() #solve(self.equations, self.base.gens())


