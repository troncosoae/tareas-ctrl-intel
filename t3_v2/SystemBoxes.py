import numpy as np

from Simulation import SimulationBox


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
