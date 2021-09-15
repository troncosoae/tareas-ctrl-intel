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


if __name__ == '__main__':
    print('running')
    pygame.init()

    clock = pygame.time.Clock()

    width, height = (1000, 600)
    Ts = 0.001
    sim = Simulation(clock, width, height, Ts, theta_0=0.3)

    # controller = BasicController()
    # controller = PIDController(-74, -110, -12, Ts)
    # controller = ExpertController(Ts)
    # controller = ExpertPIController(Ts)
    # input_sets = {
    #     'e': {
    #         'pos': FuzzySet(ramp_function_generator(0.12, 0.18)),
    #         'zer': FuzzySet(trapezoid_function_generator(-0.18, -0.12, 0.12, 0.18)),
    #         'neg': FuzzySet(ramp_function_generator(-0.12, -0.18))
    #     },
    #     'de': {
    #         'pos': FuzzySet(ramp_function_generator(0.7, 1.3)),
    #         'zer': FuzzySet(trapezoid_function_generator(-1.3, -0.7, 0.7, 1.3)),
    #         'neg': FuzzySet(ramp_function_generator(-0.7, -1.3))
    #     }
    # }
    # output_sets = {
    #     'e: pos; de: pos': FuzzySet(trapezoid_function_generator(-17, -15, -15, -13)),
    #     'e: pos; de: zer': FuzzySet(trapezoid_function_generator(-14.5, -12.5, -12.5, -10.5)),
    #     'e: pos; de: neg': FuzzySet(trapezoid_function_generator(-11, -10, -10, -9)),
    #     'e: zer; de: pos': FuzzySet(trapezoid_function_generator(-4, -2.5, -2.5, -1)),
    #     'e: zer; de: zer': FuzzySet(trapezoid_function_generator(-1.5, 0, 0, 1.5)),
    #     'e: zer; de: neg': FuzzySet(trapezoid_function_generator(1, 2.5, 2.5, 4)),
    #     'e: neg; de: pos': FuzzySet(trapezoid_function_generator(9, 10, 10, 11)),
    #     'e: neg; de: zer': FuzzySet(trapezoid_function_generator(10.5, 12.5, 12.5, 14.5)),
    #     'e: neg; de: neg': FuzzySet(trapezoid_function_generator(13, 15, 15, 17))
    # }
    # controller = FuzzyPIController(Ts, input_sets, output_sets)
    # input_sets = {
    #     'e': {
    #         'bpos': FuzzySet(ramp_function_generator(0.35, 0.36)),
    #         'mpos': FuzzySet(trapezoid_function_generator(0.25, 0.26, 0.34, 0.35)),
    #         'spos': FuzzySet(trapezoid_function_generator(0.15, 0.16, 0.24, 0.25)),
    #         'sspos': FuzzySet(trapezoid_function_generator(0.05, 0.06, 0.14, 0.15)),
    #         'zer': FuzzySet(trapezoid_function_generator(-0.05, -0.04, 0.04, 0.05)),
    #         'ssneg': FuzzySet(trapezoid_function_generator(-0.15, -0.14, -0.06, -0.05)),
    #         'sneg': FuzzySet(trapezoid_function_generator(-0.25, -0.24, -0.16, -0.15)),
    #         'mneg': FuzzySet(trapezoid_function_generator(-0.35, -0.34, -0.26, -0.25)),
    #         'bneg': FuzzySet(ramp_function_generator(-0.35, -0.36))
    #     }
    # }
    # output_sets = {
    #     'e: bpos': FuzzySet(trapezoid_function_generator(-15.5, -15, -15, -14.5)),
    #     'e: mpos': FuzzySet(trapezoid_function_generator(-8.8, -7.8, -7.8, -6.8)),
    #     'e: spos': FuzzySet(trapezoid_function_generator(-2.5, -1.5, -1.5, -0.5)),
    #     'e: sspos': FuzzySet(trapezoid_function_generator(-0.000, -0.111, -0.111, -0.222)),
    #     'e: zer': FuzzySet(trapezoid_function_generator(-0.5, -0.499, 0.499, 0.5)),
    #     'e: ssneg': FuzzySet(trapezoid_function_generator(0.222, 0.111, 0.111, 0.000)),
    #     'e: sneg': FuzzySet(trapezoid_function_generator(0.5, 1.5, 1.5, 2.5)),
    #     'e: mneg': FuzzySet(trapezoid_function_generator(6.8, 7.8, 7.8, 8.8)),
    #     'e: bneg': FuzzySet(trapezoid_function_generator(14.5, 15, 15, 15.5))
    # }
    input_sets = {
        'e': {
            'bpos': FuzzySet(ramp_function_generator(0.32, 0.4)),
            'mpos': FuzzySet(trapezoid_function_generator(0.23, 0.28, 0.32, 0.37)),
            'spos': FuzzySet(trapezoid_function_generator(0.13, 0.18, 0.22, 0.27)),
            'sspos': FuzzySet(trapezoid_function_generator(0.03, 0.08, 0.12, 0.17)),
            'zer': FuzzySet(trapezoid_function_generator(-0.07, -0.02, 0.02, 0.07)),
            'ssneg': FuzzySet(trapezoid_function_generator(-0.17, -0.12, -0.08, -0.03)),
            'sneg': FuzzySet(trapezoid_function_generator(-0.27, -0.22, -0.18, -0.13)),
            'mneg': FuzzySet(trapezoid_function_generator(-0.37, -0.32, -0.28, -0.23)),
            'bneg': FuzzySet(ramp_function_generator(-0.32, -0.4))
        }
    }
    output_sets = {
        'e: bpos': FuzzySet(trapezoid_function_generator(-15.5, -15, -15, -14.5)),
        'e: mpos': FuzzySet(trapezoid_function_generator(-8.8, -7.8, -7.8, -6.8)),
        'e: spos': FuzzySet(trapezoid_function_generator(-2.5, -1.5, -1.5, -0.5)),
        'e: sspos': FuzzySet(trapezoid_function_generator(-0.000, -0.111, -0.111, -0.222)),
        'e: zer': FuzzySet(trapezoid_function_generator(-0.5, -0.499, 0.499, 0.5)),
        'e: ssneg': FuzzySet(trapezoid_function_generator(0.222, 0.111, 0.111, 0.000)),
        'e: sneg': FuzzySet(trapezoid_function_generator(0.5, 1.5, 1.5, 2.5)),
        'e: mneg': FuzzySet(trapezoid_function_generator(6.8, 7.8, 7.8, 8.8)),
        'e: bneg': FuzzySet(trapezoid_function_generator(14.5, 15, 15, 15.5))
    }
    controller = FuzzyExpertController(Ts, input_sets, output_sets)
    sim.add_controller(controller)
    measurer = PlotingMeasurer()
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

    historical_values = measurer.get_historical_values(['theta'])
    theta_history = historical_values['theta']
    t_history = historical_values['t']
    int_theta = 0
    index = 0
    for t in t_history:
        if t > 6:
            break
        int_theta += np.abs(theta_history[index])
        index += 1
    int_theta *= Ts
    print('int_theta: ', int_theta)
    plt.plot(t_history, theta_history)
    plt.show()
    # keys = historical_values.keys()
    # for key in keys:
    #     plt.plot(
    #         np.linspace(0, 1, num=len(historical_values[key])),
    #         historical_values[key], label=key)
    # plt.xlabel('t')
    # plt.legend()
    # plt.show()
