

class BaseConstraint:

    def __init__(self, type, level):
        self.type = type
        self.level = level

    def violated(self):
        raise NotImplementedError()