from Simulation import BasicController, BasicMeasurer


class PIDController(BasicController):

    def __init__(self, kp, ki, kd, Ts):
        BasicMeasurer.__init__(self)
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.Ts = Ts
        self.int_error = 0
        self.last_error = 0

    def next_u(self, error):
        self.int_error += error*self.Ts
        der_error = (error - self.last_error)/self.Ts

        # update error values
        self.last_error = error

        return error*self.kp + self.int_error*self.ki + der_error*self.kd


class ExpertController(BasicController):

    def __init__(self):
        BasicController.__init__(self)
        self.last_error = 0

    def next_u(self, error):
        e = error
        de = error - self.last_error
        self.last_error = error
        u = 0
        if e > 0.35:
            u = -15
        elif e > 0.25:
            u = -7.8
        elif e > 0.15:
            u = -1.5
        elif e > 0.05:
            u = -0.111

        if e < -0.35:
            u = 15
        elif e < -0.25:
            u = 7.8
        elif e < -0.15:
            u = 1.5
        elif e < -0.05:
            u = 0.111

        return u
