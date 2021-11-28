from sports_scheduling.constraints.base_constraint import BaseConstraint


class RepeaterGapConstraint(BaseConstraint):

    def __init__(self, team1: str, team2: str, minimum_gap: int, penalty: int):
        """The minimum number of rounds to be played before two teams meet for the second time"""
        super().__init__(bracket='repeaterGapConstraint', level='SOFT')
        self.team1 = team1
        self.team2 = team2
        self.minimum_gap = minimum_gap
        self.penalty = penalty

    def is_violated(self):
        pass
