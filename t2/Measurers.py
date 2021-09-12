import matplotlib.pyplot as plt
import numpy as np
from Simulation import BasicMeasurer


class PlotingMeasurer(BasicMeasurer):
    def __init__(self):
        BasicMeasurer.__init__(self)
        self.t = []
        self.historical_values = {}

    def get_values(self, values_dict):
        super().get_values(values_dict)
        if 'Ts' not in values_dict:
            raise Exception("key 'Ts' must be un 'values_dict'")
        if len(self.t) == 0:
            self.t.append(0)
        else:
            self.t.append(self.t[-1] + values_dict['Ts'])
        for key in values_dict:
            value = values_dict[key]
            if key not in self.historical_values:
                self.historical_values[key] = [value]
            else:
                self.historical_values[key].append(value)

    def plot_values(self, keys=None):
        if keys is None:
            keys = self.historical_values.keys()

        for key in keys:
            plt.plot(self.t, self.historical_values[key], label=key)
        plt.xlabel('t')
        plt.legend()
        plt.show()

    def per_advance(self):
        # return super().per_advance()
        pass

    def get_historical_values(self, keys=None):
        if keys == None:
            keys = self.historical_values.keys()

        return {
            k: v for k, v in self.historical_values.items() if k in keys}
