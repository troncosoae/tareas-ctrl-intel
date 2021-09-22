from Simulation import Simulation, SimulationBox


if __name__ == "__main__":
    sim = Simulation()
    print(sim)

    box = SimulationBox('a', ['u', 'a'], ['du', 'dx'])
    print(box)
