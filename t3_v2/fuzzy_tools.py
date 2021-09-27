import numpy as np


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


def inv_trapezoid_function_generator(a, b, c, d):
    def inv_trapezoid_function(x):
        return np.min([
            np.max([
                (0 - 1)/(b - a)*(x - a) + 1,
                0,
                (1 - 0)/(d - c)*(x - c) + 0
            ]),
            1
        ])
    return inv_trapezoid_function


if __name__ == '__main__':
    func = inv_trapezoid_function_generator(1, 2, 3, 4)
    print(func(0.5))
    print(func(1.5))
    print(func(2.5))
    print(func(3.5))
    print(func(4.5))
