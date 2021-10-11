import numpy as np

from Simulation import Simulation, get_close_sim_for_box
from SystemBoxes import PendulumSystem, PHLevelSystem
from PygameBoxes import PendulumWindow, PHLevelWindow


if __name__ == "__main__":

    Ts = 0.1
    theta_0 = 0.3

    sim = Simulation()

    system = PHLevelSystem('p_sys', Ts, xi_0=3, zeta_0=2)
    pygame_tracker = PHLevelWindow(
        'pygame', ['xi', 'zeta', 'pH', 'H'], 1/Ts, get_close_sim_for_box(sim),
        speed_up=1000)

    sim.add_box(system, {'f1': 0.081, 'f2': 0.512})
    sim.add_box(pygame_tracker)

    sim.run()

    pygame_tracker.quit_pygame()
