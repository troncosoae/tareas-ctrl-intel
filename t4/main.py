import numpy as np

from Simulation import Simulation, get_close_sim_for_box
from SystemBoxes import PendulumSystem, PHLevelSystem
from PygameBoxes import PendulumWindow, PHLevelWindow
from ExtraBoxes import DerivativeBox, ConstantBox, SubtractBox
from FuzzyControlBoxes import GeneticFuzzyController


if __name__ == "__main__":

    Ts = 0.1
    theta_0 = 0.3

    sim = Simulation()

    system = PHLevelSystem('p_sys', Ts, xi_0=3, zeta_0=2)
    pygame_tracker = PHLevelWindow(
        'pygame', ['xi', 'zeta', 'pH', 'H'], 1/Ts, get_close_sim_for_box(sim),
        speed_up=1000)
    ref_box = ConstantBox('ref', 'r', 7)
    sub_box = SubtractBox('sub', 'r', 'pH', 'e')
    de_box = DerivativeBox('der', 'e')
    ctrl = GeneticFuzzyController(
        'ctrl', ['e', 'de'], ['f1', 'f2'], 'variables')

    sim.add_box(system, {'f1': 0.081, 'f2': 0.512})
    sim.add_box(pygame_tracker)

    sim.run()

    pygame_tracker.quit_pygame()
