import numpy as np

from Simulation import SimulationBox


class PendulumModel(SimulationBox):
    def __init__(self, key, Ts, **kwargs):
        SimulationBox.__init__(
            self, key, ['u', 'theta', 'theta_dot', 'x', 'x_dot', 'F'],
            ['theta_pred', 'theta_dot_pred', 'x_pred', 'x_dot_pred', 'F_pred'])
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
        # theta = input_values['theta']
        # theta_dot = input_values['theta_dot']
        # x = input_values['x']
        # x_dot = input_values['x_dot']
        # F = input_values['F']
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

        preds = {
            'theta_pred': self.state['theta'],
            'theta_dot_pred': self.state['theta_dot'],
            'x_pred': self.state['x'],
            'x_dot_pred': self.state['x_dot'],
            'F_pred': self.state['F']
        }

        # print(preds)

        return preds


class LinearPendulumModel(SimulationBox):
    def __init__(self, key, Ts, **kwargs):
        SimulationBox.__init__(
            self, key, ['u', 'theta', 'theta_dot', 'x', 'x_dot', 'F'],
            ['theta_pred', 'theta_dot_pred', 'x_pred', 'x_dot_pred', 'F_pred'])
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
        # theta = input_values['theta']
        # theta_dot = input_values['theta_dot']
        # x = input_values['x']
        # x_dot = input_values['x_dot']
        # F = input_values['F']
        theta = self.state['theta']
        theta_dot = self.state['theta_dot']
        x = self.state['x']
        x_dot = self.state['x_dot']
        F = self.state['F']

        self.state['theta'] += c['Ts']*theta_dot
        self.state['theta_dot'] += c['Ts']*(
            -c['m']*c['g']/c['M']*theta +
            1/c['M']*F
        )
        self.state['x'] += c['Ts']*x_dot
        self.state['x_dot'] += c['Ts']*(
            -(c['M'] + c['m'])*c['g']/(c['M']*c['l'])*theta +
            1/(c['M']*c['l'])*F
        )
        self.state['F'] += c['Ts']*(-100*F + 100*u)

        preds = {
            'theta_pred': self.state['theta'],
            'theta_dot_pred': self.state['theta_dot'],
            'x_pred': self.state['x'],
            'x_dot_pred': self.state['x_dot'],
            'F_pred': self.state['F']
        }

        # print(preds)

        return preds


class PendulumSubModelsModel(SimulationBox):
    def __init__(self, key, Ts, **kwargs):
        SimulationBox.__init__(
            self, key, ['u', 'theta', 'theta_dot', 'x', 'x_dot', 'F'],
            ['theta_pred', 'theta_dot_pred', 'x_pred', 'x_dot_pred', 'F_pred'])
        self.cts = {
            'Ts': Ts, 'fs': 1/Ts, 'l': 0.67, 'M': 1, 'm': 0.34, 'g': 9.8}

        self.state = {
            'F': 0,
            'theta': kwargs.get('theta_0', 0),
            'theta_dot': kwargs.get('theta_dot_0', 0),
            'x': kwargs.get('x_0', 0),
            'x_dot': kwargs.get('x_dot_0', 0),
        }

    def linear_model1(self, input_values):
        u = input_values['u']
        c = self.cts
        theta = self.state['theta']
        theta_dot = self.state['theta_dot']
        x = self.state['x']
        x_dot = self.state['x_dot']
        F = self.state['F']

        self.state['theta'] += c['Ts']*theta_dot
        self.state['theta_dot'] += c['Ts']*(
            -c['m']*c['g']/c['M']*theta +
            1/c['M']*F
        )
        self.state['x'] += c['Ts']*x_dot
        self.state['x_dot'] += c['Ts']*(
            -(c['M'] + c['m'])*c['g']/(c['M']*c['l'])*theta +
            1/(c['M']*c['l'])*F
        )
        self.state['F'] += c['Ts']*(-100*F + 100*u)

        preds = {
            'theta_pred': self.state['theta'],
            'theta_dot_pred': self.state['theta_dot'],
            'x_pred': self.state['x'],
            'x_dot_pred': self.state['x_dot'],
            'F_pred': self.state['F']
        }

        return preds

    def linear_model2(self, input_values):

        theta_0 = np.pi/4
        theta_dot_0 = 0

        u = input_values['u']
        c = self.cts
        theta = self.state['theta']
        theta_dot = self.state['theta_dot']
        x = self.state['x']
        x_dot = self.state['x_dot']
        F = self.state['F']

        m = c['m']
        M = c['M']
        l = c['l']
        g = c['g']

        self.state['theta'] += c['Ts']*theta_dot
        self.state['theta_dot'] += c['Ts']*(
            ((M+m)*c['g']*np.sin(theta_0) +
             m*l*np.cos(theta_0)*np.sin(theta_0)*theta_dot_0**2
             )*(-2*m*l*np.cos(theta_0)*np.sin(theta_0))
            /
            (m*l*np.cos(theta_0)**2 - (M + m)*l
             )*theta +
            (2*m*l*np.cos(theta_0)*np.sin(theta_0)*theta_dot_0)
            /
            (m*l*np.cos(theta_0)**2 - (M + m)*l
             )*theta_dot +
            1/(M*l)*F
        )
        self.state['x'] += c['Ts']*x_dot
        self.state['x_dot'] += c['Ts']*(
            (m*np.sin(theta_0)*(l*theta_dot_0**2-g*np.cos(theta_0)))/(
             M+m-m*l*np.cos(theta_0)**2)*theta +
            (2*m*l*np.sin(theta_0)*theta_dot_0)/(
             M+m-m*l*np.cos(theta_0))*theta_dot +
            1/(M+m+m*l*np.cos(theta_0)**2)*F
        )
        self.state['F'] += c['Ts']*(-100*F + 100*u)

        preds = {
            'theta_pred': self.state['theta'],
            'theta_dot_pred': self.state['theta_dot'],
            'x_pred': self.state['x'],
            'x_dot_pred': self.state['x_dot'],
            'F_pred': self.state['F']
        }

        return preds

    def advance(self, input_values):
        super().advance(input_values)

        if np.abs(input_values['theta']) > np.pi/8:
            print('linear model 2')
            return self.linear_model2(input_values)
        else:
            print('linear model 1')
            return self.linear_model1(input_values)
