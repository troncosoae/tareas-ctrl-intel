import numpy as np

from Simulation import SimulationBox


class InputBox(SimulationBox):
    def __init__(self, key, Ts, output_keys, **kwargs):
        SimulationBox.__init__(
            self, key, [], output_keys)
        self.output_keys = output_keys
        self.counter = 0
        self.on = True

    def advance(self, input_values):
        super().advance(input_values)
        self.counter += 1
        if self.counter > 1000:
            self.counter = 0
            self.on = not self.on
        print(self.on)
        return_dict = {}
        for key in self.output_keys:
            return_dict[key] = 1 if self.on else 0
        return return_dict


class WindModel(SimulationBox):
    def __init__(self, key, Ts, **kwargs):
        SimulationBox.__init__(
            self, key, [], ['v_m', 'v_s', 'v_ws', 'v_ts', 'v_W'])

        # TODO: check if each blade is modeled independently
        self.chars = {
            'sigma_m': kwargs.get('sigma_m', 0.1),  # slow stochastic wind var
            'sigma_s': kwargs.get('sigma_s', 0.1),  # stochastic part
            'Ts': Ts,
        }

        self.state = {
            'v_m':  kwargs.get('v_m_0', 10),  # slow stochastic wind variations
            'v_s':  kwargs.get('v_s_0', 0),  # stochastic part
            'v_ws': kwargs.get('v_ws_0', 0),  # wind shear
            'v_ts': kwargs.get('v_ts_0', 0),  # tower shadow
        }

    def advance(self, input_values):
        super().advance(input_values)
        v_m = self.state['v_m']
        v_s = self.state['v_s']
        v_ws = self.state['v_ws']
        v_ts = self.state['v_ts']

        self.state['v_m'] += np.random.normal(0, self.chars['sigma_m'])
        self.state['v_s'] += np.random.normal(0, self.chars['sigma_s'])
        v_W = self.state['v_m'] + self.state['v_s'] + self.state['v_ws'] + \
            self.state['v_ts']

        return {
            'v_m':  self.state['v_m'],
            'v_s':  self.state['v_s'],
            'v_ws': self.state['v_ws'],
            'v_ts': self.state['v_ts'],
            'v_W': v_W,
        }


class GeneratorConverterModel(SimulationBox):
    def __init__(self, key, Ts, **kwargs):
        SimulationBox.__init__(
            self, key, ['omega_g', 'tau_gr'],
            ['tau_g', 'P_g', 'tau_gm', 'omega_gm'])

        self.chars = {
            'Ts': Ts,
            'alpha_gc': kwargs.get('alpha_gc', 50),  # 50 rad/s
            'nu_g': kwargs.get('nu_g', 0.98),  # 0.98
        }

        self.state = {
            'tau_g': kwargs.get('tau_g_0', 0),
        }

    def advance(self, input_values):
        super().advance(input_values)

        tau_gr = input_values['tau_gr']
        omega_g = input_values['omega_g']
        tau_g = self.state['tau_g']
        Ts = self.chars['Ts']
        alpha_gc = self.chars['alpha_gc']
        nu_g = self.chars['nu_g']

        self.state['tau_g'] += Ts*alpha_gc*(tau_g - tau_gr)
        P_g = nu_g*omega_g*tau_g

        return {
            'tau_g': self.state['tau_g'],
            'P_g': P_g,
            'tau_gm': self.state['tau_g'],
            'omega_gm': omega_g
        }


class DriveTrainModel(SimulationBox):
    def __init__(self, key, Ts, **kwargs):
        SimulationBox.__init__(
            self, key, ['tau_r', 'tau_g'], ['omega_g', 'omega_r', 'omega_rm'])

        self.chars = {
            'Ts': Ts,
            'Bdt': kwargs.get('Bdt', 775.49),
            'Br': kwargs.get('Br', 7.11),
            'Bg': kwargs.get('Bg', 45.6),
            'Ng': kwargs.get('Ng', 95),
            'Kdt': kwargs.get('Kdt', 2.7e9),
            'nu_dt': kwargs.get('nu_dt', 0.97),
            'Jg': kwargs.get('Jg', 390),
            'Jr': kwargs.get('Jr', 55e6),
        }
        self.state = {
            'omega_r': kwargs.get('omega_r_0', 0),
            'omega_g': kwargs.get('omega_g_0', 0),
            'theta_d': kwargs.get('theta_d_0', 0),
        }

    def advance(self, input_values):
        super().advance(input_values)

        tau_r = input_values['tau_r']
        tau_g = input_values['tau_g']
        wr = self.state['omega_r']
        wg = self.state['omega_g']
        td = self.state['theta_d']
        Ts = self.chars['Ts']
        Bdt = self.chars['Bdt']
        Br = self.chars['Br']
        Bg = self.chars['Bg']
        Ng = self.chars['Ng']
        Kdt = self.chars['Kdt']
        nu_dt = self.chars['nu_dt']
        Jg = self.chars['Jg']
        Jr = self.chars['Jr']

        self.state['omega_r'] += Ts/Jr*(
            tau_r - Kdt*td - (Bdt + Br)*wr + Bdt/Ng*wg
        )
        self.state['omega_g'] += Ts/Jg*(
            nu_dt*Kdt/Ng*td + nu_dt*Bdt/Ng*wr -
            (nu_dt*Bdt/Ng**2 + Bg)*wg - tau_g
        )
        self.state['theta_d'] += Ts*(
            wr - 1/Ng*wg
        )

        return {
            'omega_g': self.state['omega_g'],
            'omega_r': self.state['omega_r'],
            'omega_rm': self.state['omega_r'],
        }


class BladePitchSystem(SimulationBox):
    def __init__(self, key, Ts, **kwargs):
        SimulationBox.__init__(
            self, key, ['v_W', 'beta_r', 'omega_r'], ['beta_m', 'tau_r'])

        def default_Cq(lmbda, beta):
            return 0.45*np.cos(beta)/lmbda

        self.chars = {
            'zeta': kwargs.get('zeta', 0.6),  # damping factor
            'omega': kwargs.get('omega', 11.11),  # natural freq
            'ro': kwargs.get('ro', 1.225),  # ro
            'R': kwargs.get('R', 57.5),  # R (m)
            'Cq': kwargs.get('Cq', default_Cq),  # Cq(lambda, beta)
            'Ts': Ts,
        }
        self.state = {
            'beta_m': kwargs.get('beta_m_0', 0),
            'beta_m_dot': kwargs.get('beta_m_dot_0', 0),
        }

    def advance(self, input_values):
        super().advance(input_values)
        br = input_values['beta_r']
        v_W = input_values['v_W']
        bm = self.state['beta_m']
        bm_dot = self.state['beta_m_dot']
        Ts = self.chars['Ts']
        z = self.chars['zeta']
        w = self.chars['omega']
        ro = self.chars['ro']
        R = self.chars['R']
        Cq = self.chars['Cq']

        self.state['beta_m'] += Ts*bm_dot
        self.state['beta_m_dot'] += Ts*(
            br*w**2 - 2*z*w*bm_dot - w**2*bm
        )

        lmbda = w*R/v_W
        tau_r = (ro*np.pi*R**3*Cq(lmbda, bm)*v_W**2)/2

        return {
            'tau_r': tau_r,
            'beta_m': self.state['beta_m'],
        }


class PendulumSystem(SimulationBox):
    def __init__(self, key, Ts, **kwargs):
        SimulationBox.__init__(
            self, key, ['u'], ['theta', 'theta_dot', 'x', 'x_dot', 'F'])
        self.cts = {
            'Ts': Ts, 'fs': 1/Ts, 'l': 0.67, 'M': 1, 'm': 0.34, 'g': 9.8}

        self.state = {
            'F': 0,
            'theta': kwargs.get('theta_0', 0),
            'theta_dot': kwargs.get('theta_dot_0', 0),
            'x': kwargs.get('x_0', 0),
            'x_dot': kwargs.get('x_dot_0', 0),
        }

    def advance(self, input_values):
        super().advance(input_values)
        u = input_values['u']
        c = self.cts
        theta = self.state['theta']
        theta_dot = self.state['theta_dot']
        x = self.state['x']
        x_dot = self.state['x_dot']
        F = self.state['F']

        self.state['theta'] += c['Ts']*theta_dot
        self.state['theta_dot'] += c['Ts']*(
            (
                (c['M'] + c['m'])*c['g']*np.sin(theta) +
                (F + c['m']*c['l']*np.sin(theta)*theta_dot**2)*np.cos(theta)
            )/(
                - c['m']*c['l']*np.cos(theta)**2 + (c['M'] + c['m'])*c['l']
            )
        )
        self.state['x'] += c['Ts']*x_dot
        self.state['x_dot'] += c['Ts']*(
            (
                F + c['m']*c['l']*np.sin(theta)*theta_dot**2 -
                c['m']*c['g']*np.cos(theta)*np.sin(theta)
            )/(
                -c['M'] + c['m'] + c['m']*np.cos(theta)**2
            )
        )
        self.state['F'] += c['Ts']*(-100*F + 100*u)

        return {
            'theta': self.state['theta'],
            'theta_dot': self.state['theta_dot'],
            'x': self.state['x'],
            'x_dot': self.state['x_dot'],
            'F': self.state['F']
        }
