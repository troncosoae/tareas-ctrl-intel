import numpy as np

from Simulation import Simulation, get_close_sim_for_box
from SystemBoxes import PendulumSystem, WindModel, BladePitchSystem, \
    InputBox, DriveTrainModel, GeneratorConverterModel
from PygameBoxes import PendulumWindow, TurbineWindow, PlottingTurbineWindow
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
    blade_pitch_system = BladePitchSystem('bp_sys', Ts)
    drive_train_model = DriveTrainModel('dt_model', Ts)
    generator_converter_model = GeneratorConverterModel('gc_model', Ts)
    measurer = PlottingMeasurer(
        'meas',
        [
            'v_m', 'v_s', 'v_ws', 'v_ts', 'v_W', 'beta_m', 'beta_r', 'omega_r',
            'omega_g', 'P_g', 'tau_g'
        ],
        Ts)
    pygame_tracker = PlottingTurbineWindow(
        'pygame', {
            'v_W': (255, 255, 255),
            'omega_g': (255, 255, 0),
            'beta_r': (255, 0, 0)
        },
        -1, 20, pygame_fs, get_close_sim_for_box(sim))
    input_box = InputBox('inpt_box', Ts, ['beta_r'])

    sim.add_box(wind_model)
    sim.add_box(blade_pitch_system, {'beta_r': np.pi/8, 'omega_r': 0})
    sim.add_box(drive_train_model, {'tau_g': 0})
    sim.add_box(generator_converter_model, {'tau_gr': 0})
    sim.add_box(measurer)
    sim.add_box(pygame_tracker)
    sim.add_box(input_box)

    sim.run()

    pygame_tracker.quit_pygame()

    measurer.plot_values()
    # measurer.plot_values(['P_g'])
