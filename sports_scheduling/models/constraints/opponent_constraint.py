from typing import List

from numpy import ndarray

from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team


class OpponentConstraint(BaseConstraint):

    def __init__(self, team_id: id, opponent_id: int, matchweek: int, penalty: int):
        """Forbid a team to play against an opponent in a given matchweek"""
        super().__init__(bracket='opponentConstraint', level='SOFT')
        self.team_id = team_id
        self.opponent_id = opponent_id
        self.matchweek = matchweek
        self.penalty = penalty

    def is_violated(self, teams: List[Team], fixture_table: ndarray) -> bool:

