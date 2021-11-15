import numpy as np

from Simulation import Simulation, get_close_sim_for_box
from SystemBoxes import WindModel, BladePitchSystem, \
    InputBox, DriveTrainModel, GeneratorConverterModel
from PygameBoxes import PlottingTurbineWindow
from MeasuringBoxes import PlottingMeasurer
from ControlBoxes import PIDController, TurbineController


if __name__ == "__main__":

    Ts = 0.001
    pygame_fs = 1/Ts
    theta_0 = np.pi

    tau_gr_stable = 0.1
    beta_r_stable = 0.1
    omega_g_stable = 0.1
    # omega_gr_stable = omega_g_stable

    sim = Simulation()

    wind_model = WindModel('wind_model', Ts)
    blade_pitch_system = BladePitchSystem('bp_sys', Ts)
    drive_train_model = DriveTrainModel(
        'dt_model', Ts,
        omega_g_0=omega_g_stable)
    generator_converter_model = GeneratorConverterModel('gc_model', Ts)
    omega_g_ctrl = TurbineController(
        'omega_g_ctrl', kp=10000, ki=1, kd=0, Ts=Ts)
    measurer = PlottingMeasurer(
        'meas',
        [
            'v_W', 'beta_m', 'beta_r', 'omega_r',
            'omega_g', 'P_g', 'tau_g', 'tau_r', 'tau_gr',
            'theta_d'
        ],
        Ts)
    pygame_tracker = PlottingTurbineWindow(
        'pygame', {
            # 'omega_gr': (255, 255, 255),
            'omega_g': (255, 255, 0),
            'beta_r': (255, 0, 0),
        },
        -0.5, 1.5, pygame_fs, get_close_sim_for_box(sim))

    sim.add_box(wind_model)
    sim.add_box(
        blade_pitch_system, {'beta_r': beta_r_stable, 'omega_r': 1})
    sim.add_box(drive_train_model, {'tau_g': 1})
    sim.add_box(generator_converter_model, {'tau_gr': tau_gr_stable})
    sim.add_box(omega_g_ctrl, {'P_r': 0.1})
    sim.add_box(measurer)
    sim.add_box(pygame_tracker)

    sim.run()

    pygame_tracker.quit_pygame()

    measurer.plot_values(exclude={'tau_r'})
    # measurer.plot_values({'P_g', 'P_r', 'tau_gr'})
    measurer.plot_values({'omega_g', 'beta_r', 'tau_gr'})
    measurer.plot_values(
        {'omega_r', 'omega_g', 'tau_r', 'tau_g', 'theta_d'},
        exclude={'tau_r', 'tau_g'})
