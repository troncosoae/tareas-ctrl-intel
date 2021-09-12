import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from Simulation import BasicController


class FuzzySet:
    def __init__(self, membership_function=lambda x: 0):
        self.membership_function = membership_function

    def membership_value(self, x):
        return self.membership_function(x)


class FuzzyPIController(BasicController):
    def __init__(self, Ts, input_sets, output_sets):
        BasicController.__init__(self)
        self.Ts = Ts
        self.last_error = 0
        self.int_error = 0
        self.input_sets = input_sets
        self.output_sets = output_sets

    def fuzzify_inputs(self, inputs):
        if inputs.keys() != self.input_sets.keys():
            raise Exception('inputs keys must be the same!')
        membership_values = {}
        for input_key in inputs:
            input_value = inputs[input_key]
            inputs_sets = self.input_sets[input_key]
            membership_values_for_key = {}
            for set_key in inputs_sets:
                membership_values_for_key[set_key] = \
                    inputs_sets[set_key].membership_value(input_value)
            membership_values[input_key] = membership_values_for_key
        print(membership_values)
        return membership_values

    def inference_model(self, membership_values):
        e_membership_values = membership_values['e']
        de_membership_values = membership_values['de']

        output_functions = []
        for e_set_key in e_membership_values:
            for de_set_key in de_membership_values:
                output_set = self.output_sets[
                    f'e: {e_set_key}; de: {de_set_key}']
                # print(output_set.membership_function(12.5), e_membership_values[e_set_key], de_membership_values[de_set_key])
                # print(np.min([
                #     output_set.membership_function(12.5),
                #     e_membership_values[e_set_key],
                #     de_membership_values[de_set_key]
                # ]))

                def get_output_function(e_set_key, de_set_key, membership_function):
                    def output_function(x):
                        return np.min([
                            membership_function(x),
                            e_membership_values[e_set_key],
                            de_membership_values[de_set_key]
                        ])
                    return output_function
                output_function = get_output_function(e_set_key, de_set_key, output_set.membership_function)

                # print('l1', output_function(12.5))

                output_functions.append(output_function)

        print([f(12.5) for f in output_functions])
        return output_functions

    def defuzzification(self, output_functions):
        def output_function(x):
            return np.max([f(x) for f in output_functions])
        # test = 12.5
        # print([f(test) for f in output_functions])
        # print(f'output_function({test})', output_function(test))
        # x_list = np.linspace(-20, 20, num=2000)
        # y_list = [output_function(x) for x in x_list]
        # plt.plot(x_list, y_list)
        # plt.show()
        int_fx = quad(lambda x: output_function(x)*x, -20, 20)[0]
        int_f = quad(lambda x: output_function(x), -20, 20)[0]
        if int_f == 0:
            int_f = 1e-10
        out = int_fx/int_f
        return out

    def next_u(self, error):
        e = error
        de = (error - self.last_error)/self.Ts
        ie = self.int_error + error
        self.int_error = ie
        self.last_error = error

        membership_values = self.fuzzify_inputs({'e': e, 'de': de})
        output_functions = self.inference_model(membership_values)
        u = self.defuzzification(output_functions)

        print(f'e: {e:5.5}, de: {de:5.5} -> u: {u:5.5}')

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
    # ramp = ramp_function_generator(1, 2)
    # print(ramp(0.5))
    # print(ramp(1.5))
    # print(ramp(2.5))
    # ramp = ramp_function_generator(2, 1)
    # print(ramp(0.5))
    # print(ramp(1.5))
    # print(ramp(2.5))
    # print('-----')
    # trapezoid = trapezoid_function_generator(1, 2, 4, 5)
    # print(trapezoid(0.5))
    # print(trapezoid(1.5))
    # print(trapezoid(3))
    # print(trapezoid(4.5))
    # print(trapezoid(5.5))
    # print(quad(trapezoid, 0, 10))
    # trapezoid = trapezoid_function_generator(1.5, 1.51, 4.5, 4.51)
    # print(trapezoid(0.5))
    # print(trapezoid(1.5))
    # print(trapezoid(3))
    # print(trapezoid(4.5))
    # print(trapezoid(5.5))
    # print(quad(trapezoid, 0, 10))
    fs = FuzzySet()
    print(fs.membership_value(0))
