from sports_scheduling.constraints.base_constraint import BaseConstraint


class FairnessConstraint(BaseConstraint):

    def __init__(self):
        """TBD"""
        super().__init__(bracket='fairnessConstraint', level='SOFT')

    def is_violated(self):
        pass
