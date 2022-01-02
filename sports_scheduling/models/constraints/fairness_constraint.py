from typing import List

from numpy import ndarray

from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team
from sports_scheduling.util import get_team_by_index, contains_n_consecutive_numbers


class FairnessConstraint(BaseConstraint):

    def __init__(self, consecutive_hard_matches: int, penalty: int):
        """No C-class team should play more than ``consecutive_hard_matches`` consecutive matches against A-class team"""
        super().__init__(bracket='fairnessConstraint', level='SOFT')

        assert isinstance(consecutive_hard_matches, int) and isinstance(penalty, int)
        self.consecutive_hard_matches = consecutive_hard_matches
        self.penalty = penalty

    def is_violated(self, teams: List[Team], fixture_table: ndarray) -> bool:
        for team in teams:
            assert team.category in ['A', 'B', 'C', None], f'unrecognized category for team {vars(team)}'

            # Fairness constraint is only applied to third class teams
            if team.category == 'C':
                tough_opponent_matchweeks = []
                for opponent_index, matchweek in enumerate(fixture_table[team.assigned_index]):
                    # get all home games against class A teams
                    if get_team_by_index(teams, opponent_index).category == 'A':
                        tough_opponent_matchweeks.append(matchweek)

                for opponent_index, matchweek in enumerate(fixture_table[:, team.assigned_index]):
                    # get all away games against class A teams
                    if get_team_by_index(teams, opponent_index).category == 'A':
                        tough_opponent_matchweeks.append(matchweek)

                # Check if three consecutive matchweeks are present in the schedule with tough opponents
                if contains_n_consecutive_numbers(tough_opponent_matchweeks, self.consecutive_hard_matches + 1):
                    return True

        return False
