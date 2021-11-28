from sports_scheduling.models.constraints.base_constraint import BaseConstraint


class RepeaterGapConstraint(BaseConstraint):

    def __init__(self, team1_id: int, team2_id: int, minimum_gap: int, penalty: int):
        """The minimum number of rounds to be played before two teams meet for the second time"""
        super().__init__(bracket='repeaterGapConstraint', level='SOFT')
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.minimum_gap = minimum_gap
        self.penalty = penalty

    def is_violated(self):
        pass
