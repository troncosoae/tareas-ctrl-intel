import pygame
import time
from Simulation import Simulation, BasicMeasurer
from AutomaticControllers import PIDControler
from Measurers import PlotingMeasurer


if __name__ == '__main__':
    print('running')
    pygame.init()

    clock = pygame.time.Clock()

    width, height = (1000, 600)
    Ts = 0.001
    sim = Simulation(clock, width, height, Ts)

    controller = PIDControler(-74, -110, -12, Ts)
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
    measurer.plot_values(['theta'])
