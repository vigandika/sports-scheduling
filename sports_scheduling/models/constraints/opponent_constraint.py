from typing import List

from numpy import ndarray

from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team
from sports_scheduling.util import get_team_by_id


class OpponentConstraint(BaseConstraint):

    def __init__(self, team_id: id, opponent_id: int, matchweek: int, penalty: int):
        """Forbid a team to play against an opponent in a given matchweek"""
        super().__init__(bracket='opponentConstraint', level='SOFT')

        assert isinstance(team_id, int) and isinstance(opponent_id, int) and isinstance(matchweek, int) and isinstance(penalty, int)
        self.team_id = team_id
        self.opponent_id = opponent_id
        self.matchweek = matchweek
        self.penalty = penalty

    def is_violated(self, teams: List[Team], fixture_table: ndarray) -> bool:
        team = get_team_by_id(teams, self.team_id)
        opponent = get_team_by_id(teams, self.opponent_id)
        assert getattr(team, 'assigned_index') is not None and getattr(opponent, 'assigned_index') is not None, \
            f"either team with id {team.id} or opponent with id {opponent.id} have no assigned_index property"

        # If a match between the two teams in the constraint is assigned to the constraint matchweek, the constraint is violated
        if fixture_table[team.assigned_index, opponent.assigned_index] == self.matchweek or \
                fixture_table[opponent.assigned_index, team.assigned_index] == self.matchweek:
            return True

        return False
