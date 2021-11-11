import numpy as np

from Simulation import SimulationBox


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
