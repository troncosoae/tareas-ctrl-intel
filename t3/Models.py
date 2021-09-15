class Model:
    def __init__(self, advance=None):
        self.advance = advance
        if self.advance is None:
            def default_advance(x, u):
                return
            self.advance = default_advance

    def advance(self, x, u):
        return self.advance(x, u)

    def simulate(self, values):
        if 't' not in values:
            raise KeyError("'values' variable must have key 't'")
        # TODO: verify that has all variables
        for t in values['t']:
            print(t)
            self.advance(0, 0)
