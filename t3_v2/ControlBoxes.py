from Simulation import SimulationBox


class PIDController(SimulationBox):

    def __init__(self, key, kp, ki, kd, Ts):
        SimulationBox.__init__(
            self, key, ['ref', 'theta'], ['u'])
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.Ts = Ts
        self.int_error = 0
        self.last_error = 0

    def advance(self, input_values):
        super().advance(input_values)
        error = input_values['theta'] - input_values['ref']
        self.int_error += error*self.Ts
        der_error = (error - self.last_error)/self.Ts

        # update error values
        self.last_error = error

        u = error*self.kp + self.int_error*self.ki + der_error*self.kd
        print('u', u)
        return {'u': u}
