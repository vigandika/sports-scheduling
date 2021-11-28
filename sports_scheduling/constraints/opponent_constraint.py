from sports_scheduling.constraints.base_constraint import BaseConstraint


class OpponentConstraint(BaseConstraint):

    def __init__(self):
        """Forbid a team to play against an opponent in a given matchweek"""
        super().__init__(bracket='opponentConstraint', level='SOFT')

    def is_violated(self):
        pass

