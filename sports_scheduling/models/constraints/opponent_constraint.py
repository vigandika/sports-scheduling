from sports_scheduling.models.constraints.base_constraint import BaseConstraint


class OpponentConstraint(BaseConstraint):

    def __init__(self, team: str, opponent: str, matchweek: int, penalty: int):
        """Forbid a team to play against an opponent in a given matchweek"""
        super().__init__(bracket='opponentConstraint', level='SOFT')
        self.team = team
        self.opponent = opponent
        self.matchweek = matchweek
        self.penalty = penalty

    def is_violated(self):
        pass
