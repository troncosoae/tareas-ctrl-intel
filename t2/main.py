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
            'pos': FuzzySet(ramp_function_generator(0.15, 0.16)),
            'zer': FuzzySet(trapezoid_function_generator(-0.15, -0.14, 0.14, 0.15)),
            'neg': FuzzySet(ramp_function_generator(-0.15, -0.16))
        },
        'de': {
            'pos': FuzzySet(ramp_function_generator(1, 1.1)),
            'zer': FuzzySet(trapezoid_function_generator(-1, -0.9, 0.9, 1)),
            'neg': FuzzySet(ramp_function_generator(-1, -1.1))
        }
    }
    output_sets = {
        # 'e: pos; de: pos': FuzzySet(trapezoid_function_generator(-15.5, -15, -15, -14.5)),
        # 'e: pos; de: zer': FuzzySet(trapezoid_function_generator(-13, -12.5, -12.5, -12)),
        # 'e: pos; de: neg': FuzzySet(trapezoid_function_generator(-10.5, -10, -10, -9.5)),
        # 'e: zer; de: pos': FuzzySet(trapezoid_function_generator(-3, -2.5, -2.5, -2)),
        # 'e: zer; de: zer': FuzzySet(trapezoid_function_generator(-0.5, 0, 0, 0.5)),
        # 'e: zer; de: neg': FuzzySet(trapezoid_function_generator(2, 2.5, 2.5, 3)),
        # 'e: neg; de: pos': FuzzySet(trapezoid_function_generator(9.5, 10, 10, 10.5)),
        # 'e: neg; de: zer': FuzzySet(trapezoid_function_generator(12, 12.5, 12.5, 13)),
        # 'e: neg; de: neg': FuzzySet(trapezoid_function_generator(14.5, 15, 15, 15.5))
        'e: pos; de: pos': FuzzySet(trapezoid_function_generator(-20, -15, -15, -10)),
        'e: pos; de: zer': FuzzySet(trapezoid_function_generator(-15, -12.5, -12.5, -10)),
        'e: pos; de: neg': FuzzySet(trapezoid_function_generator(-15, -10, -10, -5)),
        'e: zer; de: pos': FuzzySet(trapezoid_function_generator(-5, -2.5, -2.5, 0)),
        'e: zer; de: zer': FuzzySet(trapezoid_function_generator(-5, 0, 0, 5)),
        'e: zer; de: neg': FuzzySet(trapezoid_function_generator(0, 2.5, 2.5, 5)),
        'e: neg; de: pos': FuzzySet(trapezoid_function_generator(5, 10, 10, 15)),
        'e: neg; de: zer': FuzzySet(trapezoid_function_generator(10, 12.5, 12.5, 15)),
        'e: neg; de: neg': FuzzySet(trapezoid_function_generator(10, 15, 15, 20))
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
