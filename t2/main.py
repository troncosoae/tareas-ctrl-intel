import pygame
import time
import numpy as np
import matplotlib.pyplot as plt
from Simulation import Simulation
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
    sim = Simulation(clock, width, height, Ts, theta_0=-0.3)

    # controller = PIDController(-74, -110, -12, Ts)
    # controller = ExpertPIController(Ts)
    input_sets = {
        'e': {
            'bpos': FuzzySet(ramp_function_generator(0.35, 0.36)),
            'mpos': FuzzySet(trapezoid_function_generator(0.25, 0.26, 0.34, 0.35)),
            'spos': FuzzySet(trapezoid_function_generator(0.15, 0.16, 0.24, 0.25)),
            'sspos': FuzzySet(trapezoid_function_generator(0.05, 0.06, 0.14, 0.15)),
            'zer': FuzzySet(trapezoid_function_generator(-0.05, -0.04, 0.04, 0.05)),
            'ssneg': FuzzySet(trapezoid_function_generator(-0.15, -0.14, -0.06, -0.05)),
            'sneg': FuzzySet(trapezoid_function_generator(-0.25, -0.24, -0.16, -0.15)),
            'mneg': FuzzySet(trapezoid_function_generator(-0.35, -0.34, -0.26, -0.25)),
            'bneg': FuzzySet(ramp_function_generator(-0.35, -0.36))
        }
    }
    output_sets = {
        'e: bpos': FuzzySet(trapezoid_function_generator(-15.5, -15, -15, -14.5)),
        'e: mpos': FuzzySet(trapezoid_function_generator(-8.8, -7.8, -7.8, -6.8)),
        'e: spos': FuzzySet(trapezoid_function_generator(-2.5, -1.5, -1.5, -0.5)),
        'e: sspos': FuzzySet(trapezoid_function_generator(-0.000, -0.111, -0.111, -0.222)),
        'e: zer': FuzzySet(trapezoid_function_generator(-1.5, 0, 0, 1.5)),
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

    while not sim.is_closed():
        start_time = time.time()

        sim.tick_clock()
        sim.handle_events()
        sim.advance_simulation()
        sim.refresh_window()
        # print(f'loop: {time.time() - start_time}s')

    pygame.quit()
    measurer.plot_values(['theta', 'theta_dot'])

    # historical_values = measurer.get_historical_values()
    # keys = historical_values.keys()
    # for key in keys:
    #     plt.plot(
    #         np.linspace(0, 1, num=len(historical_values[key])),
    #         historical_values[key], label=key)
    # plt.xlabel('t')
    # plt.legend()
    # plt.show()
