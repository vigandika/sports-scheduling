from typing import List

from numpy import ndarray

from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team
from sports_scheduling.util import get_team_by_id


class RepeaterGapConstraint(BaseConstraint):

    def __init__(self, team1_id: int, team2_id: int, minimum_gap: int, penalty: int):
        """The minimum number of rounds to be played before two teams meet for the second time"""
        super().__init__(bracket='repeaterGapConstraint', level='SOFT')

        assert isinstance(team1_id, int) and isinstance(team2_id, int) and isinstance(minimum_gap, int) and isinstance(penalty, int)
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.minimum_gap = minimum_gap
        self.penalty = penalty

    def is_violated(self, teams: List[Team], fixture_table: ndarray) -> bool:
        team_1 = get_team_by_id(teams, self.team1_id)
        team_2 = get_team_by_id(teams, self.team2_id)
        assert getattr(team_1, 'assigned_index') is not None and getattr(team_2, 'assigned_index') is not None, \
            f"either team with id {team_1.id} or team with id {team_2.id} have no assigned_index property"

        first_game = fixture_table[team_1.assigned_index, team_2.assigned_index]
        second_game = fixture_table[team_2.assigned_index, team_1.assigned_index]

        if abs(first_game - second_game) < self.minimum_gap:
            # If there are less than `self.minimum_gap` matchweeks between the two matches of the two teams, the constraint is violated
            return True
        else:
            return False
