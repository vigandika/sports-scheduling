from sports_scheduling.models.constraints.base_constraint import BaseConstraint


class ParticipationConstraint(BaseConstraint):

    def __init__(self):
        """Every team should play exactly once at each matchweek"""
        super().__init__(bracket='participationConstraint', level='HARD')

    def is_violated(self):
        pass
