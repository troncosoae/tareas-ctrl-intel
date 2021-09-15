import pygame
import time
import numpy as np
import matplotlib.pyplot as plt
from Simulation import BasicController, Simulation
from AutomaticControllers import PIDController, ExpertController, \
    ExpertPIController
from FuzzyTools import FuzzyPIController, FuzzyExpertController, FuzzySet, \
    trapezoid_function_generator, ramp_function_generator
from Measurers import PlotingMeasurer
from Models import Model


if __name__ == '__main__':
    print('running')
    pygame.init()

    clock = pygame.time.Clock()

    width, height = (1000, 600)
    Ts = 0.001
    sim = Simulation(clock, width, height, Ts, theta_0=0.3)

    # controller = BasicController()
    controller = PIDController(-74, -110, -12, Ts)
    measurer = PlotingMeasurer()

    sim.add_controller(controller)
    sim.add_measurer(measurer)

    sim.refresh_window()

    t = 0
    while not sim.is_closed():
        start_time = time.time()

        sim.tick_clock()
        sim.handle_events()
        sim.advance_simulation()
        sim.refresh_window()
        # print(f'loop: {time.time() - start_time}s')
        if t % 100 == 0:
            print('-------------------')
            print(f'at time: {t*Ts}')
            print('-------------------')
        t += 1

    pygame.quit()
    measurer.plot_values(['theta', 'theta_dot'])

    model = Model()

    historical_values = measurer.get_historical_values(['theta'])
    # theta_history = historical_values['theta']
    # t_history = historical_values['t']
    # int_theta = 0
    # index = 0
    # for t in t_history:
    #     if t > 6:
    #         break
    #     int_theta += np.abs(theta_history[index])
    #     index += 1
    # int_theta *= Ts
    # print('int_theta: ', int_theta)
    # plt.plot(t_history, theta_history)
    # plt.show()

    model.simulate(historical_values)


