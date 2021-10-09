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
    theta_0 = np.pi

    sim = Simulation()

    pendulum_system = PendulumSystem('p_sys', Ts, theta_0=theta_0)
    pygame_tracker = PendulumWindow(
        'pygame', ['x', 'theta'], 1/Ts, get_close_sim_for_box(sim))
    # pid_controller = PIDController(
    #     'pid', 'ref', 'theta', 'u', -74, -110, -12, Ts)
    lqr_controller = LQRController(
        'lqr', ['theta', 'theta_dot', 'F'], 'u',
        {'theta': -29.5, 'theta_dot': -7.20, 'F': 0.107})
    lqrsubmdl_controller = LQRSubmodelController(
        'lqr', ['theta', 'theta_dot', 'F'], 'u',
        {'theta': -29.5, 'theta_dot': -7.20, 'F': 0.107},
        {'theta': -23.7, 'theta_dot': -6.60, 'F': 0.0987},
        {'theta': -33.7, 'theta_dot': -7.61, 'F': 0.112})
    lqrsubmdlfzy_controller = LQRSubmodelFuzzyController(
        'lqr', ['theta', 'theta_dot', 'F'], 'u',
        {'theta': -29.5, 'theta_dot': -7.20, 'F': 0.107},
        {'theta': -23.7, 'theta_dot': -6.60, 'F': 0.0987},
        {'theta': -33.7, 'theta_dot': -7.61, 'F': 0.112})
    # measurer = PlottingMeasurer('meas', ['u', 'theta', 'theta_pred'], Ts)
    measurer = PlottingMeasurer(
        'meas',
        [
            'u', 'theta', 'theta_pred', 'theta_dot', 'theta_dot_pred', 'x',
            'x_pred', 'F', 'F_pred'],
        Ts)
    pendulum_model = PendulumSubModelsModel('model', Ts, theta_0=theta_0)
    # pendulum_model = LinearPendulumModel('model', Ts, theta_0=theta_0)
    # pendulum_model = PendulumModel('model', Ts, theta_0=-0.29)

    sim.add_box(pendulum_system, {'u': 0})
    # sim.add_box(pid_controller, {'ref': 0})
    # sim.add_box(lqr_controller)
    # sim.add_box(lqrsubmdl_controller)
    sim.add_box(lqrsubmdlfzy_controller)
    sim.add_box(pendulum_model)
    sim.add_box(measurer)
    sim.add_box(pygame_tracker)

    sim.run()

    pygame_tracker.quit_pygame()

    measurer.plot_values([
        'theta'])
    measurer.plot_values([
        'theta', 'theta_pred', 'theta_dot', 'theta_dot_pred'])

    u = measurer.historical_values['u']
    theta = measurer.historical_values['theta']
    theta_dot = measurer.historical_values['theta_dot']
    F = measurer.historical_values['F']
    t = measurer.t

    # print(u, theta)
    int_theta = 0
    J = 0
    index = 0
    for ti in t:
        if ti > 6:
            break
        int_theta += np.abs(theta[index])
        J += theta[index]**2*50 + theta_dot[index]**2*10 + \
            F[index]**2*0.01 + u[index]**2*1
        index += 1
    int_theta *= Ts

    print(f'int_theta: {int_theta}\nJ: {J}')
