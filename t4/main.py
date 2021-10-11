import numpy as np

from Simulation import Simulation, get_close_sim_for_box
from SystemBoxes import PendulumSystem, PHLevelSystem
from PygameBoxes import PendulumWindow, PHLevelWindow
from ExtraBoxes import DerivativeBox, ConstantBox, SubtractBox
from FuzzyControlBoxes import GeneticFuzzyController


if __name__ == "__main__":

    Ts = 0.1
    theta_0 = 0.3

    sim = Simulation(max_iters=1000)

    system = PHLevelSystem('p_sys', Ts, xi_0=3, zeta_0=2)
    pygame_tracker = PHLevelWindow(
        'pygame', ['xi', 'zeta', 'pH', 'H'], 1/Ts, get_close_sim_for_box(sim),
        speed_up=1000)
    ref_box = ConstantBox('ref', 'r', 7)
    sub_box = SubtractBox('sub', 'r', 'pH', 'e')
    de_box = DerivativeBox('der', 'e', Ts)
    ctrl_box = GeneticFuzzyController(
        'ctrl', ['e', 'de'], ['f1', 'f2'], [ 2.42939944,  4.2990003 ,  5.62900667,  6.74092919,  8.93234742,
       10.78758332, 12.80918742,  2.68018242,  4.21389581,  6.20339832,
        7.88525808,  8.66076684, 10.33675192, 10.90875974,  6.04496709,
        3.78618774,  3.44633474,  4.84972392,  5.75434955,  4.63448859,
        3.39926357,  6.05317803,  1.18194578,  4.11691108,  3.6993171 ,
        5.95210012,  6.12156426,  3.00287238,  5.17766304,  5.53873667,
        4.17945443,  7.17181301])

    sim.add_box(system, {'f1': 0.081, 'f2': 0.512})
    sim.add_box(pygame_tracker)
    sim.add_box(ref_box)
    sim.add_box(sub_box)
    sim.add_box(de_box)
    sim.add_box(ctrl_box)

    sim.run()

    pygame_tracker.quit_pygame()

    print(ctrl_box.get_performance())
