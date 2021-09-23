from Simulation import Simulation, SimulationBox
from Boxes import PygameBox, bx2


if __name__ == "__main__":
    sim = Simulation()
    print(sim)

    box = SimulationBox('a', ['u', 'a'], ['du', 'dx'])
    print(box)

    box1 = PygameBox('b', ['u', 'a'])
    print(box1)

    box2 = bx2('c')
    print(box2)

    sim.add_box(box, {'u': 2, 'a': 0.2})
    sim.add_box(box1)
    sim.add_box(box2)

    sim.run()

    sim.print_diagram()
    print(sim.signals.keys())
    print(sim.boxes.keys())
