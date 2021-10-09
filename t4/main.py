import numpy as np

from Simulation import Simulation, get_close_sim_for_box
from SystemBoxes import PendulumSystem
from PygameBoxes import PendulumWindow
from ControlBoxes import PIDController, LQRController, LQRSubmodelController
from MeasuringBoxes import PlottingMeasurer
from ModelBoxes import PendulumModel, LinearPendulumModel, \
    PendulumSubModelsModel
from FuzzyControlBoxes import LQRSubmodelFuzzyController


if __name__ == "__main__":

    Ts = 0.001
    theta_0 = 0.3

    sim = Simulation()

    pendulum_system = PendulumSystem('p_sys', Ts, theta_0=theta_0)
    pygame_tracker = PendulumWindow(
        'pygame', ['x', 'theta'], 1/Ts, get_close_sim_for_box(sim))

    sim.add_box(pendulum_system, {'u': 0})
    sim.add_box(pygame_tracker)

    sim.run()

    pygame_tracker.quit_pygame()
