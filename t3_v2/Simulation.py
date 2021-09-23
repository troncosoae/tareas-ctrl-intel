class Simulation:
    def __init__(self):
        self.boxes = {}
        self.signals = {}
        self.advance_order = []

    def __str__(self):
        return 'Simulation'

    def print_diagram(self):
        for box_key in self.advance_order:
            for signal_key in self.boxes[box_key].inputs_keys:
                print(self.signals[signal_key])
            print(self.boxes[box_key])
            for signal_key in self.boxes[box_key].outputs_keys:
                print(self.signals[signal_key])

    def add_box(self, box, initial_signals_dict={}):
        # add a box, check correct signals, consider order of forward
        # With each box, signals are created for each output
        # Total:
        # initial existing signals
        # add box -> create new signals with initial values
        # add to position on in adavane order (somehow)
        if type(box) is not SimulationBox and \
                not issubclass(type(box), SimulationBox):
            raise Exception(
                "'box' argument must be of class " +
                "'SimulationBox' or inherit from it")
        if box.key in self.boxes:
            raise Exception(
                "key of box is already used, please use a unique key... ")

        # add box to boxes
        self.boxes[box.key] = box
        self.advance_order.append(box.key)

        # add input signals
        for signal_key in box.inputs_keys:
            # verify: signals exist
            # if dont exist, then must have intial value
            if signal_key not in self.signals:
                if signal_key not in initial_signals_dict:
                    raise Exception(f"if '{signal_key}' hasn't been added, " +
                                    "then inital values must be provided")
                if (not isinstance(
                        initial_signals_dict[signal_key], float) and
                    not isinstance(
                        initial_signals_dict[signal_key], int)):
                    raise Exception("inital values must be 'int' or 'float'")
                self.signals[signal_key] = SimulationSignal(
                    signal_key, None,
                    initial_values=initial_signals_dict[signal_key])

        for signal_key in box.outputs_keys:
            # verify signals dont exist
            # if exist, check if origin is None (edit), else raise error
            if signal_key in self.signals:
                if self.signals[signal_key].origin_box_key is not None:
                    raise Exception(
                        f"signal '{signal_key}' already has origin...")
                self.signals[signal_key].origin_box_key = box.key
            self.signals[signal_key] = SimulationSignal(signal_key, box.key)

    def advance(self):
        for box_key in self.advance_order:
            print(box_key)

    def run(self):
        iteration = 0
        while iteration < 10:
            print(f'it: {iteration}')
            self.advance()

            iteration += 1


class SimulationBox:
    def __init__(self, key, inputs_keys, outputs_keys):
        self.key = key
        self.inputs_keys = inputs_keys
        self.outputs_keys = outputs_keys

    def __str__(self):
        return '({})\t -> \t[{}]\t -> \t({})'.format(
            ';\t'.join(self.inputs_keys),
            self.key,
            ';\t'.join(self.outputs_keys)
        )

    def advance(self):
        # uses values of signals
        # returns values of output signals
        pass


class SimulationSignal:
    def __init__(self, key, origin_box_key, initial_values=None):
        self.key = key
        self.origin_box_key = origin_box_key
        self.initial_values = initial_values

    def __str__(self):
        return 'S([{}] -> {})'.format(
            self.origin_box_key,
            self.key
        )
