from sports_scheduling.constraints.base_constraint import BaseConstraint


class StaticVenueConstraint(BaseConstraint):

    def __init__(self):
        """Limit the number of consecutive games a team can play in the same venue"""
        super().__init__(bracket='staticVenueConstraint', level='HARD')

    def is_violated(self):
        pass
