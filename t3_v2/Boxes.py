from Simulation import SimulationBox


class PygameBox(SimulationBox):
    def __init__(self, key, inputs_keys):
        SimulationBox.__init__(self, key, inputs_keys, [])


class bx2(PygameBox):
    def __init__(self, key):
        SimulationBox.__init__(self, key, [], [])
