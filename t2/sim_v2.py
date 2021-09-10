import pygame
import math
import time
import numpy as np
import time

# @https://github.com/keychali/pendulum-simulation/blob/master/forvideo.py


class Simulation:
    def __init__(self, clock, window_w, window_h, Ts):
        self.clock = clock
        self.window_w = window_w
        self.window_h = window_h
        self.window = pygame.display.set_mode((self.window_w, self.window_h))
        self.closed = False

        self.pixel_m_ratio = 100

        self.cts = {
            'Ts': Ts, 'fs': 1/Ts, 'l': 0.67, 'M': 1, 'm': 0.34, 'g': 9.8}

        self.F = 0
        self.theta = 0.1
        self.theta_dot = 0
        self.x = 0
        self.x_dot = 0

    def xy_coordinates(self):
        y_pend2car = np.cos(self.theta)*self.cts['l']
        x_pend2car = np.sin(self.theta)*self.cts['l']
        # TODO: change for calculating x
        x_car = self.x
        y_car = 0
        x_pend = x_pend2car + x_car
        y_pend = y_pend2car + y_car
        return x_pend, y_pend, x_car, y_car

    def map_xy2window(self, x_pend, y_pend, x_car, y_car):
        w = self.window_w
        h = self.window_h
        print(
            f'xp:{x_pend:5.4f}, yp:{y_pend:5.4f}, \
            x:{x_car:5.4f}, y:{y_car:5.4f}')
        return (
            x_pend*self.pixel_m_ratio + w/2,
            h/2 - y_pend*self.pixel_m_ratio,
            x_car*self.pixel_m_ratio + w/2,
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
        u = 0

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
                c['M'] + c['m'] - c['m']*np.cos(theta)**2
            )
        )
        self.F += c['Ts']*(-100*F + 100*u)

    def tick_clock(self):
        self.clock.tick(self.cts['fs'])

    def handle_events(self):
        print(pygame.event.get())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()

    def is_closed(self):
        return self.closed

    def close(self):
        self.closed = True


if __name__ == '__main__':
    print('running')
    pygame.init()

    clock = pygame.time.Clock()

    width, height = (1000, 600)
    Ts = 0.001
    sim = Simulation(clock, width, height, Ts)
    sim.refresh_window()

    while not sim.is_closed():
        start_time = time.time()

        sim.tick_clock()
        sim.handle_events()
        sim.advance_simulation()
        sim.refresh_window()
        print(f'loop: {time.time() - start_time}s')

    pygame.quit()
