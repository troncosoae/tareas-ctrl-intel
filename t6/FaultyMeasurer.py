import numpy as np

from Simulation import SimulationBox


class FaultyMeasurer(SimulationBox):

    def __init__(self, key, Ts, fault_freq):
        super().__init__(key, ['tau_g'], ['tau_gm', 'faulty'])
        self.Ts = Ts
        self.count_max = fault_freq/Ts
        self.counter = 0
        self.on_fault = False
        self.fault_dir_pos = False
        self.last_delta = 0

    def advance(self, input_values):
        super().advance(input_values)

        self.counter += 1
        if self.counter > self.count_max:
            self.counter = 0
            self.on_fault = np.random.choice([True, False])
            self.fault_dir_pos = np.random.choice([True, False])
            print(self.on_fault, self.fault_dir_pos)

        tau_gm = input_values['tau_g']
        if self.on_fault:
            tau_gm += np.random.normal(30000, 1) if self.fault_dir_pos else \
                np.random.normal(-30000, 1)

        return {
            'tau_gm': tau_gm,
            'faulty': 1 if self.on_fault else 0
        }
