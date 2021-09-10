from Simulation import BasicController


class PIDControler(BasicController):

    def __init__(self, kp, ki, kd, Ts):
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
