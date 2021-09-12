import numpy as np
from scipy.integrate import quad
from Simulation import BasicController


class FuzzySet:
    def __init__(self, membership_funcion):
        self.mf = membership_funcion

    def membership_value(self, x):
        return self.mf(x)


class FuzzyController(BasicController):
    def __init__(self, input_keys=[]):
        BasicController.__init__(self)
        self.sets = {input_key: [] for input_key in input_keys}

    def add_set(self, input_key, fuzzy_set):
        self.sets[input_key].append(fuzzy_set)

    def fuzzify_inputs(self, inputs):
        if inputs.keys() != self.sets.keys():
            raise Exception('inputs keys must be the same!')

    def next_u(self, error):
        u = 0
        return u


def ramp_function_generator(a, b):
    def ramp_function(x):
        return np.max([
            np.min([
                (1 - 0)/(b - a)*(x - a) + 0,
                1
            ]),
            0
        ])
    return ramp_function


def trapezoid_function_generator(a, b, c, d):
    def trapezoid_function(x):
        return np.max([
            np.min([
                (1 - 0)/(b - a)*(x - a) + 0,
                1,
                (0 - 1)/(d - c)*(x - c) + 1
            ]),
            0
        ])
    return trapezoid_function


if __name__ == '__main__':
    ramp = ramp_function_generator(1, 2)
    print(ramp(0.5))
    print(ramp(1.5))
    print(ramp(2.5))
    ramp = ramp_function_generator(2, 1)
    print(ramp(0.5))
    print(ramp(1.5))
    print(ramp(2.5))
    print('-----')
    trapezoid = trapezoid_function_generator(1, 2, 4, 5)
    print(trapezoid(0.5))
    print(trapezoid(1.5))
    print(trapezoid(3))
    print(trapezoid(4.5))
    print(trapezoid(5.5))
    print(quad(trapezoid, 0, 10))
    trapezoid = trapezoid_function_generator(1.5, 1.51, 4.5, 4.51)
    print(trapezoid(0.5))
    print(trapezoid(1.5))
    print(trapezoid(3))
    print(trapezoid(4.5))
    print(trapezoid(5.5))
    print(quad(trapezoid, 0, 10))
