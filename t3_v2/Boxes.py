import numpy as np
import pygame

from Simulation import SimulationBox


class PygameBox(SimulationBox):
    def __init__(self, key, inputs_keys, fs, **kwargs):
        SimulationBox.__init__(self, key, inputs_keys, [])

        pygame.init()
        self.clock = pygame.time.Clock()
        self.fs = fs
        self.pixel_m_ratio = 100
        self.width = kwargs.get('width', 1000)
        self.height = kwargs.get('height', 600)
        self.window = pygame.display.set_mode((self.width, self.height))
        self.close = False

    def xy_coordinates(self, x, theta):
        print(f't:{theta:.2f}\tx:{x:.2f}')
        y_pend2car = np.cos(theta)*0.67
        x_pend2car = np.sin(theta)*0.67
        x_car = x
        y_car = 0
        x_pend = x_pend2car + x_car
        y_pend = y_pend2car + y_car
        return x_pend, y_pend, x_car, y_car

    def map_xy2window(self, x_pend, y_pend, x_car, y_car):
        w = self.width
        h = self.height
        return (
            (x_pend*self.pixel_m_ratio + w/2) % w,
            h/2 - y_pend*self.pixel_m_ratio,
            (x_car*self.pixel_m_ratio + w/2) % w,
            h/2 - y_car*self.pixel_m_ratio
        )

    def refresh_window(self, x, theta):
        x_pend, y_pend, x_car, y_car = self.xy_coordinates(x, theta)
        x_pend, y_pend, x_car, y_car = self.map_xy2window(
            x_pend, y_pend, x_car, y_car)

        self.window.fill((0, 0, 0))

        pygame.draw.lines(
            self.window, (10, 255, 255), False,
            [(x_pend, y_pend), (x_car, y_car)], 2
        )
        pygame.draw.lines(
            self.window, (255, 255, 255), False,
            [(self.width/2, 0), (self.width/2, self.height)], 1
        )
        pygame.draw.circle(
            self.window, (255, 10, 255),
            (x_pend, y_pend), 7
        )
        pygame.draw.circle(
            self.window, (255, 255, 10),
            (x_car, y_car), 10
        )

        pygame.display.update()

    def handle_events(self):
        pass

    def advance(self, input_values):
        super().advance(input_values)
        self.clock.tick(self.fs)
        self.refresh_window(input_values['x'], input_values['theta'])
        print(input_values)
        return {}


class PendulumSystem(SimulationBox):
    def __init__(self, key, Ts, **kwargs):
        SimulationBox.__init__(
            self, key, ['u'], ['theta', 'theta_dot', 'x', 'x_dot'])
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
            'x_dot': self.state['x_dot']
        }
