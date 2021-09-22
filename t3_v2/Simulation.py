class Simulation:
    def __init__(self):
        self.boxes = {}
        self.signals = {}
        self.advance_order = []

    def __str__(self):
        return 'Simulation'

    def add_box(self, box):
        # TODO: add a box, check correct signals, consider order of forward
        # With each box, signals are created for each output
        # Total:
        # initial existing signals
        # add box -> create new signals with initial values
        # add to position on in adavane order (somehow)
        pass

    def advance(self):
        for element in self.advance_order:
            print(type(element))


class SimulationBox:
    def __init__(self, key, inputs_keys, outputs_keys):
        self.key = key
        self.inputs_keys = inputs_keys
        self.outputs_keys = outputs_keys

    def __str__(self):
        return '[{}]:\tinputs:  \t{}\n\toutputs:  \t{}'.format(
            self.key,
            ';\t'.join(self.inputs_keys),
            ';\t'.join(self.outputs_keys)
        )

    def advance(self):
        # uses values of signals
        # returns values of output signals
        pass


class SimulationSignal:
    def __init__(self, key, initial_values):
        self.key = key
        self.initial_values = initial_values

    def __str__(self):
        return self.key
