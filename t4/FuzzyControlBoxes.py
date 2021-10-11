import numpy as np
from numpy.core.fromnumeric import var

from Simulation import SimulationBox
from fuzzy_tools import ramp_function_generator, \
    trapezoid_function_generator, inv_trapezoid_function_generator, \
    triangle_function_generator


class GeneticFuzzyController(SimulationBox):
    def __init__(self, key, inputs_keys, outputs_keys, variables, delta=0.3):
        super().__init__(key, inputs_keys, outputs_keys)

        self.int_e = 0
        self.delta = delta
        self.iters2delta = None
        self.iters = 0

        self.variables = variables

        e_vars = variables[0:7]
        de_vars = variables[7:14]
        f1_vars = variables[14:23]
        f2_vars = variables[23:32]

        self.e_sets_dict = {
            'se': ramp_function_generator(e_vars[0], e_vars[2]),
            'ze': triangle_function_generator(
                e_vars[1], e_vars[3], e_vars[5]),
            'be': ramp_function_generator(e_vars[6], e_vars[4])
        }
        self.de_sets_dict = {
            'sde': ramp_function_generator(de_vars[0], de_vars[2]),
            'zde': triangle_function_generator(
                de_vars[1], de_vars[3], de_vars[5]),
            'bde': ramp_function_generator(de_vars[6], de_vars[4])
        }

        self.f1_dict = {
            'sesde': f1_vars[0],
            'sezde': f1_vars[1],
            'sebde': f1_vars[2],
            'zesde': f1_vars[3],
            'zezde': f1_vars[4],
            'zebde': f1_vars[5],
            'besde': f1_vars[6],
            'bezde': f1_vars[7],
            'bebde': f1_vars[8]
        }
        self.f2_dict = {
            'sesde': f2_vars[0],
            'sezde': f2_vars[1],
            'sebde': f2_vars[2],
            'zesde': f2_vars[3],
            'zezde': f2_vars[4],
            'zebde': f2_vars[5],
            'besde': f2_vars[6],
            'bezde': f2_vars[7],
            'bebde': f2_vars[8]
        }

    def advance(self, input_values):
        super().advance(input_values)

        e = input_values['e']
        de = input_values['de']

        self.iters += 1
        self.int_e += np.abs(e)
        if e < self.delta and self.iters2delta is None:
            self.iters2delta = self.iters
        elif e > self.delta:
            self.iters2delta = None

        f1 = 0
        sum_p_f1 = 0
        f2 = 0
        sum_p_f2 = 0
        # print(f'e={e:.2f}   de={de:.2f}')
        for set_e_key in self.e_sets_dict:
            for set_de_key in self.de_sets_dict:
                comp_set_key = set_e_key + set_de_key
                p_e = self.e_sets_dict[set_e_key](e)
                p_de = self.de_sets_dict[set_de_key](de)
                f1_temp = self.f1_dict[comp_set_key]
                f2_temp = self.f2_dict[comp_set_key]
                # print(
                #     f'e_key:{set_e_key}, de_key:{set_de_key} --> ' +
                #     f'p_e:{p_e:.2f}   p_de:{p_de:.2f}')
                f1 += p_e*p_de*f1_temp
                sum_p_f1 += p_e*p_de
                f2 += p_e*p_de*f2_temp
                sum_p_f2 += p_e*p_de
        f1 = f1/sum_p_f1
        f2 = f2/sum_p_f2

        # print(f'e={e:.2f}   de={de:.2f}   f1={f1:.2f}   f2={f2:.2f}')
        # print('------------------------------------------------')
        return {
            'f1': f1,
            'f2': f2
        }

    def get_performance(self):
        return {
            'int_e': self.int_e, 'iters2delta': self.iters2delta,
            'variables': self.variables}


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
