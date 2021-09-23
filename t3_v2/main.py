from Simulation import Simulation, SimulationBox
from SystemBoxes import PendulumSystem
from PygameBoxes import PendulumWindow
from ControlBoxes import PIDController


if __name__ == "__main__":

    Ts = 0.001

    sim = Simulation()
    # print(sim)

    # box = SimulationBox('a', ['u', 'a'], ['du', 'dx'])
    # print(box)

    # box1 = PygameBox('b', ['u', 'a'])
    # print(box1)

    # box2 = bx2('c')
    # print(box2)

    pendulum_system = PendulumSystem('p_sys', Ts, theta_0=0.3)
    pygame_tracker = PendulumWindow('pygame', ['x', 'theta'], 1/Ts)
    pid_controller = PIDController('pid', -74, -110, -12, Ts)

    sim.add_box(pendulum_system, {'u': 0})
    print('u', sim.signals['u'].value)
    sim.add_box(pid_controller, {'ref': 0})
    print('u', sim.signals['u'].value)
    sim.add_box(pygame_tracker)

    print(sim.advance_order)

    # sim.add_box(box, {'u': 2, 'a': 0.2})
    # sim.add_box(box1)
    # sim.add_box(box2)

    sim.run()

    sim.print_diagram()
    print(sim.signals.keys())
    print(sim.boxes.keys())
