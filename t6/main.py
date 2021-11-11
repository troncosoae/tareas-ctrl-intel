import numpy as np

from Simulation import Simulation, get_close_sim_for_box
from SystemBoxes import PendulumSystem, WindModel
from PygameBoxes import PendulumWindow, TurbineWindow
from ControlBoxes import PIDController, LQRController, LQRSubmodelController
from MeasuringBoxes import PlottingMeasurer
from ModelBoxes import PendulumModel, LinearPendulumModel, \
    PendulumSubModelsModel
from FuzzyControlBoxes import LQRSubmodelFuzzyController


if __name__ == "__main__":

    Ts = 0.001
    pygame_fs = 1/Ts
    theta_0 = np.pi

    sim = Simulation()

    wind_model = WindModel('wind_model', Ts)
    measurer = PlottingMeasurer(
        'meas',
        ['v_m', 'v_s', 'v_ws', 'v_ts', 'v_W'],
        Ts)
    pygame_tracker = TurbineWindow(
        'pygame', [], pygame_fs, get_close_sim_for_box(sim))

    sim.add_box(wind_model)
    sim.add_box(measurer)
    sim.add_box(pygame_tracker)

    sim.run()

    pygame_tracker.quit_pygame()

    measurer.plot_values(['v_m', 'v_s', 'v_ws', 'v_ts', 'v_W'])
