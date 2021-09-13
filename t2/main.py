import pygame
import time
import numpy as np
import matplotlib.pyplot as plt
from Simulation import Simulation
from AutomaticControllers import PIDController, ExpertController, \
    ExpertPIController
from FuzzyTools import FuzzyPIController, FuzzySet, \
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
            'pos': FuzzySet(ramp_function_generator(0.12, 0.18)),
            'zer': FuzzySet(trapezoid_function_generator(-0.18, -0.12, 0.12, 0.18)),
            'neg': FuzzySet(ramp_function_generator(-0.12, -0.18))
        },
        'de': {
            'pos': FuzzySet(ramp_function_generator(0.7, 1.3)),
            'zer': FuzzySet(trapezoid_function_generator(-1.3, -0.7, 0.7, 1.3)),
            'neg': FuzzySet(ramp_function_generator(-0.7, -1.3))
        }
    }
    output_sets = {
        'e: pos; de: pos': FuzzySet(trapezoid_function_generator(-17, -15, -15, -13)),
        'e: pos; de: zer': FuzzySet(trapezoid_function_generator(-14.5, -12.5, -12.5, -10.5)),
        'e: pos; de: neg': FuzzySet(trapezoid_function_generator(-11, -10, -10, -9)),
        'e: zer; de: pos': FuzzySet(trapezoid_function_generator(-4, -2.5, -2.5, -1)),
        'e: zer; de: zer': FuzzySet(trapezoid_function_generator(-1.5, 0, 0, 1.5)),
        'e: zer; de: neg': FuzzySet(trapezoid_function_generator(1, 2.5, 2.5, 4)),
        'e: neg; de: pos': FuzzySet(trapezoid_function_generator(9, 10, 10, 11)),
        'e: neg; de: zer': FuzzySet(trapezoid_function_generator(10.5, 12.5, 12.5, 14.5)),
        'e: neg; de: neg': FuzzySet(trapezoid_function_generator(13, 15, 15, 17))
    }
    controller = FuzzyPIController(Ts, input_sets, output_sets)
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
