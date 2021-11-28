from sports_scheduling.constraints.base_constraint import BaseConstraint


class RepeaterGapConstraint(BaseConstraint):

    def __init__(self):
        """The minimum number of rounds to be played before two teams meet for the second time"""
        super().__init__(bracket='repeaterGapConstraint', level='SOFT')

    def is_violated(self):
        pass
