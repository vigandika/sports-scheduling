class BaseConstraint:

    def __init__(self, bracket, level):
        self.bracket = bracket
        self.level = level

    def is_violated(self):
        raise NotImplementedError()
