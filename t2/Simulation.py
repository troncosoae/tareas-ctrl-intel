import pygame
import math
import time
import numpy as np
import time

# @https://github.com/keychali/pendulum-simulation/blob/master/forvideo.py


class BasicController:
    def __init__(self):
        pass

    def __str__(self):
        return 'BasicController...'

    def next_u(self, error):
        return 0


class BasicMeasurer:
    def __init__(self):
        self.last_values_dict = {}

    def __str__(self):
        return 'BasicMeasurer...'

    def get_values(self, values_dict):
        self.last_values_dict = values_dict

    def print_values(self):
        print_str = ''
        for key in self.last_values_dict:
            value = self.last_values_dict[key]
            print_str += f'{key}: {value:5.4f}\t'
        print(print_str)

    def per_advance(self):
        self.print_values()


class Simulation:
    def __init__(
            self, clock, window_w, window_h, Ts, *args, **kwargs):
        self.clock = clock
        self.window_w = window_w
        self.window_h = window_h
        self.window = pygame.display.set_mode((self.window_w, self.window_h))
        self.closed = False

        self.pixel_m_ratio = 100

        self.controller = None
        self.measurer = None

        self.cts = {
            'Ts': Ts, 'fs': 1/Ts, 'l': 0.67, 'M': 1, 'm': 0.34, 'g': 9.8}

        self.u = 0
        self.F = 0
        self.theta = kwargs.get('theta_0', 0.3)
        self.theta_dot = kwargs.get('theta_dot_0', 0)
        self.x = kwargs.get('x_0', 0)
        self.x_dot = kwargs.get('x_dot_0', 0)

    def xy_coordinates(self):
        y_pend2car = np.cos(self.theta)*self.cts['l']
        x_pend2car = np.sin(self.theta)*self.cts['l']
        x_car = self.x
        y_car = 0
        x_pend = x_pend2car + x_car
        y_pend = y_pend2car + y_car
        return x_pend, y_pend, x_car, y_car

    def map_xy2window(self, x_pend, y_pend, x_car, y_car):
        w = self.window_w
        h = self.window_h

        return (
            (x_pend*self.pixel_m_ratio + w/2) % w,
            h/2 - y_pend*self.pixel_m_ratio,
            (x_car*self.pixel_m_ratio + w/2) % w,
            h/2 - y_car*self.pixel_m_ratio
        )

    def refresh_window(self):
        x_pend, y_pend, x_car, y_car = self.xy_coordinates()
        x_pend, y_pend, x_car, y_car = self.map_xy2window(
            x_pend, y_pend, x_car, y_car)

        self.window.fill((0, 0, 0))

        pygame.draw.lines(
            self.window, (10, 255, 255), False,
            [(x_pend, y_pend), (x_car, y_car)], 2
        )
        pygame.draw.lines(
            self.window, (255, 255, 255), False,
            [(self.window_w/2, 0), (self.window_w/2, self.window_h)], 1
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

    def advance_simulation(self):
        c = self.cts
        theta = self.theta
        theta_dot = self.theta_dot
        x = self.x
        x_dot = self.x_dot
        F = self.F
        u = self.u

        self.theta += c['Ts']*theta_dot
        self.theta_dot += c['Ts']*(
            (
                (c['M'] + c['m'])*c['g']*np.sin(theta) +
                (F + c['m']*c['l']*np.sin(theta)*theta_dot**2)*np.cos(theta)
            )/(
                - c['m']*c['l']*np.cos(theta)**2 + (c['M'] + c['m'])*c['l']
            )
        )
        self.x += c['Ts']*x_dot
        self.x_dot += c['Ts']*(
            (
                F + c['m']*c['l']*np.sin(theta)*theta_dot**2 -
                c['m']*c['g']*np.cos(theta)*np.sin(theta)
            )/(
                -c['M'] + c['m'] + c['m']*np.cos(theta)**2
            )
        )
        self.F += c['Ts']*(-100*F + 100*u)

        # work additional devices
        self.devices_advance()

    def tick_clock(self):
        self.clock.tick(self.cts['fs'])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.close()
                if event.key == pygame.K_r:
                    self.reset()

    def is_closed(self):
        return self.closed

    def close(self):
        self.closed = True

    def reset(self):
        self.u = 0
        self.F = 0
        self.theta = 0
        self.theta_dot = 0
        self.x = 0
        self.x_dot = 0

    def get_state(self):
        return {
            'u': self.u,
            'F': self.F,
            'theta': self.theta,
            'theta_dot': self.theta_dot,
            'x': self.x,
            'x_dot': self.x_dot,
            'Ts': self.cts['Ts']
        }

    def devices_advance(self):
        if self.controller is not None:
            error = self.theta - 0
            self.u = self.controller.next_u(error)
        else:
            self.u = 0

        if self.measurer is not None:
            self.measurer.get_values(self.get_state())
            self.measurer.per_advance()

    def add_controller(self, controller):
        if 'next_u' not in dir(controller):
            raise Exception("controller attribute must have 'next_u' method..")
        self.controller = controller

    def add_measurer(self, measurer):
        if 'get_values' not in dir(measurer) or \
                'per_advance' not in dir(measurer):
            raise Exception("controller attribute must have 'get_values'\
                 method and 'per_advance' method..")
        self.measurer = measurer


if __name__ == '__main__':
    print('running')
    pygame.init()

    clock = pygame.time.Clock()

    width, height = (1000, 600)
    Ts = 0.001
    sim = Simulation(clock, width, height, Ts)
    sim.refresh_window()
    basic_control = BasicController()
    basic_measurer = BasicMeasurer()
    sim.add_controller(basic_control)
    sim.add_measurer(basic_measurer)

    while not sim.is_closed():
        start_time = time.time()

        sim.tick_clock()
        sim.handle_events()
        sim.advance_simulation()
        sim.refresh_window()
        print(f'loop: {time.time() - start_time}s')

    pygame.quit()
