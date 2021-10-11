import numpy as np

from Simulation import SimulationBox
from fuzzy_tools import ramp_function_generator, \
    trapezoid_function_generator, inv_trapezoid_function_generator, \
    triangle_function_generator


class GeneticFuzzyController(SimulationBox):
    def __init__(self, key, inputs_keys, outputs_keys, variables):
        super().__init__(key, inputs_keys, outputs_keys)

        self.e_sets_dict = {
            'se': ramp_function_generator(1, 3),
            'ze': triangle_function_generator(2, 3, 4),
            'be': ramp_function_generator(3, 5)
        }
        self.de_sets_dict = {
            'sde': ramp_function_generator(1, 3),
            'zde': triangle_function_generator(2, 3, 4),
            'bde': ramp_function_generator(3, 5)
        }

        self.f1_dict = {
            'sesde': 1,
            'sezde': 1,
            'sebde': 1,
            'zesde': 1,
            'zezde': 1,
            'zebde': 1,
            'besde': 1,
            'bezde': 1,
            'bebde': 1
        }
        self.f2_dict = {
            'sesde': 1,
            'sezde': 1,
            'sebde': 1,
            'zesde': 1,
            'zezde': 1,
            'zebde': 1,
            'besde': 1,
            'bezde': 1,
            'bebde': 1
        }

    def advance(self, input_values):
        super().advance(input_values)
        return {
            'f1': 1,
            'f2': 1
        }


class LQRSubmodelFuzzyController(SimulationBox):

    def __init__(self, key, inputs_keys, man_v_name, K1, K2, K3):
        SimulationBox.__init__(
            self, key, inputs_keys, [man_v_name])
        self.man_v_name = man_v_name

        self.K1 = K1
        self.K2 = K2
        self.K3 = K3

        self.K2_trap_theta_func = inv_trapezoid_function_generator(
            -np.pi/4, 0, 0, np.pi/4)
        self.K3_trap_theta_dot_func = inv_trapezoid_function_generator(
            -2, -1, 1, 2)

    def advance(self, input_values):
        super().advance(input_values)

        # print(self.K2_trap_theta_func(np.pi/8))
        # print(self.K2_trap_theta_func(0.01))
        # print(self.K3_trap_theta_dot_func(1.5))
        # print(self.K3_trap_theta_dot_func(0))

        theta = input_values['theta']
        theta_dot = input_values['theta_dot']

        set2_bel = self.K2_trap_theta_func(theta)
        set3_bel = self.K3_trap_theta_dot_func(theta_dot)
        set1_bel = 1 - set2_bel*set3_bel
        total_bel = set1_bel + set2_bel + set3_bel

        u1 = 0
        for k in self.inputs_keys:
            u1 += self.K1[k]*input_values[k]

        u2 = 0
        for k in self.inputs_keys:
            u2 += self.K2[k]*input_values[k]

        u3 = 0
        for k in self.inputs_keys:
            u3 += self.K3[k]*input_values[k]

        u = (u1*set1_bel + u2*set2_bel + u3*set3_bel)/total_bel

        # K = self.K1
        # if (np.abs(input_values['theta']) > np.pi/8 and
        #         np.abs(input_values['theta_dot']) < 1.5):
        #     # print('K2')
        #     K = self.K2
        # elif (np.abs(input_values['theta']) <= np.pi/8 and
        #         np.abs(input_values['theta_dot']) >= 1.5):
        #     K = self.K3
        #     # print('K3')
        # # else:
        # #     print('K1')

        # u = 0
        # for k in self.inputs_keys:
        #     u += K[k]*input_values[k]

        return {self.man_v_name: u}
