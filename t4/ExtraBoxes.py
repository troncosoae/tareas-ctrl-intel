import numpy as np

from Simulation import SimulationBox


class DerivativeBox(SimulationBox):
    def __init__(self, key, input_key, Ts):
        self.input_key = input_key
        self.output_key = 'd' + input_key
        self.prev_value = 0
        self.Ts = Ts
        super().__init__(key, [input_key], [self.output_key])

    def advance(self, input_values):
        super().advance(input_values)
        value = input_values[self.input_key]
        der = (value - self.prev_value)/self.Ts
        self.prev_value = value
        return {
            self.output_key: der
        }


class ConstantBox(SimulationBox):
    def __init__(self, key, output_key, constant):
        self.output_key = output_key
        self.value = constant
        super().__init__(key, [], [self.output_key])

    def advance(self, input_values):
        super().advance(input_values)
        return {
            self.output_key: self.value
        }


class SubtractBox(SimulationBox):
    def __init__(self, key, input_key1, input_key2, output_key):
        self.output_key = output_key
        self.input_key1 = input_key1
        self.input_key2 = input_key2
        super().__init__(key, [], [self.output_key])

    def advance(self, input_values):
        super().advance(input_values)
        return {
            self.output_key: input_values[self.input_key1] -
            input_values[self.input_key2]
        }
