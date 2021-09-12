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


class ExpertPIController(BasicController):
    def __init__(self, Ts):
        self.Ts = Ts
        self.last_error = 0
        self.int_error = 0

    def next_u(self, error):
        e = error
        de = (error - self.last_error)/self.Ts
        ie = self.int_error + error
        self.int_error = ie
        self.last_error = error

        print(f'de:{de:5.3}')

        u = 0
        if e > 0.15:
            u = -12.5
            if de > 1:
                u -= 2.5
            if de < -1:
                u += 2.5
        elif e > 0:
            u = 0
            if de > 1:
                u -= 2.5
            if de < -1:
                u += 2.5

        if e < -0.15:
            u = 12.5
            if de > 1:
                u -= 2.5
            if de < -1:
                u += 2.5
        elif e < 0:
            u = 0
            if de > 1:
                u -= 2.5
            if de < -1:
                u += 2.5

        return u


class ExpertController(BasicController):

    def __init__(self, Ts):
        BasicController.__init__(self)
        self.last_error = 0
        self.int_error = 0
        self.Ts = Ts

    def next_u(self, error):
        e = error
        de = (error - self.last_error)/self.Ts
        self.last_error = error
        ie = self.int_error + error*self.Ts
        self.int_error = ie
        u = 0
        if e > 0.35:
            u = -15
        elif e > 0.25:
            u = -7.8
        elif e > 0.15:
            u = -1.5
        elif e > 0.05:
            u = -0.111
        elif e > 0:
            u = e*-74 + de*-110
            # u = e*-74 + de*-110 + ie*-12

        if e < -0.35:
            u = 15
        elif e < -0.25:
            u = 7.8
        elif e < -0.15:
            u = 1.5
        elif e < -0.05:
            u = 0.111
        elif e < 0:
            u = e*-74 + de*-110
            # u = e*-74 + de*-110 + ie*-12

        return u
