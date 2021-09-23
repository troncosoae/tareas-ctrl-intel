from Simulation import Simulation, get_close_sim_for_box
from SystemBoxes import PendulumSystem
from PygameBoxes import PendulumWindow
from ControlBoxes import PIDController


if __name__ == "__main__":

    Ts = 0.001

    sim = Simulation()

    pendulum_system = PendulumSystem('p_sys', Ts, theta_0=0.3)
    pygame_tracker = PendulumWindow(
        'pygame', ['x', 'theta'], 1/Ts, get_close_sim_for_box(sim))
    pid_controller = PIDController(
        'pid', 'ref', 'theta', 'u', -74, -110, -12, Ts)

    sim.add_box(pendulum_system, {'u': 0})
    sim.add_box(pid_controller, {'ref': 0})
    sim.add_box(pygame_tracker)

    sim.run()

    pygame_tracker.quit_pygame()

    sim.print_diagram()
    print(sim.signals.keys())
    print(sim.boxes.keys())
