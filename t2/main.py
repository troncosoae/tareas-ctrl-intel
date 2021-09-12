import pygame
import time
import numpy as np
import matplotlib.pyplot as plt
from Simulation import Simulation
from AutomaticControllers import PIDController, ExpertController, \
    ExpertPIController
from Measurers import PlotingMeasurer


if __name__ == '__main__':
    print('running')
    pygame.init()

    clock = pygame.time.Clock()

    width, height = (1000, 600)
    Ts = 0.001
    sim = Simulation(clock, width, height, Ts, theta_0=-0.3)

    # controller = PIDController(-74, -110, -12, Ts)
    controller = ExpertPIController(Ts)
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
