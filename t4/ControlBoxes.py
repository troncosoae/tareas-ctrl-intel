import numpy as np

from Simulation import SimulationBox


class PIDController(SimulationBox):

    def __init__(self, key, ref_name, ctrl_v_name, man_v_name, kp, ki, kd, Ts):
        SimulationBox.__init__(
            self, key, [ref_name, ctrl_v_name], [man_v_name])
        self.ref_name = ref_name
        self.ctrl_v_name = ctrl_v_name
        self.man_v_name = man_v_name

        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.Ts = Ts
        self.int_error = 0
        self.last_error = 0

    def advance(self, input_values):
        super().advance(input_values)
        error = input_values[self.ctrl_v_name] - input_values[self.ref_name]
        self.int_error += error*self.Ts
        der_error = (error - self.last_error)/self.Ts

        # update error values
        self.last_error = error

        u = error*self.kp + self.int_error*self.ki + der_error*self.kd
        return {self.man_v_name: u}


class LQRController(SimulationBox):

    def __init__(self, key, inputs_keys, man_v_name, K):
        SimulationBox.__init__(
            self, key, inputs_keys, [man_v_name])
        self.man_v_name = man_v_name

        self.K = K

    def advance(self, input_values):
        super().advance(input_values)

        u = 0
        for k in self.inputs_keys:
            u += self.K[k]*input_values[k]

        return {self.man_v_name: u}


class LQRSubmodelController(SimulationBox):

    def __init__(self, key, inputs_keys, man_v_name, K1, K2, K3):
        SimulationBox.__init__(
            self, key, inputs_keys, [man_v_name])
        self.man_v_name = man_v_name

        self.K1 = K1
        self.K2 = K2
        self.K3 = K3

    def advance(self, input_values):
        super().advance(input_values)

        K = self.K1
        if (np.abs(input_values['theta']) > np.pi/8 and
                np.abs(input_values['theta_dot']) < 1.5):
            # print('K2')
            K = self.K2
        elif (np.abs(input_values['theta']) <= np.pi/8 and
                np.abs(input_values['theta_dot']) >= 1.5):
            K = self.K3
            # print('K3')
        # else:
        #     print('K1')

        u = 0
        for k in self.inputs_keys:
            u += K[k]*input_values[k]

        return {self.man_v_name: u}
