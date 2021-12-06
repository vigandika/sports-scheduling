from typing import List

from numpy import ndarray

from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team


class ParticipationConstraint(BaseConstraint):

    def __init__(self):
        """Every team should play exactly once at each matchweek"""
        super().__init__(bracket='participationConstraint', level='HARD')

    def is_violated(self, teams: List[Team], fixture_table: ndarray):
        no_of_matchweeks = (len(teams) - 1) * 2
        for team in teams:
            assert getattr(team, 'assigned_index') is not None, f"team {team.name} needs to have an 'assigned_index'"
            for matchweek in range(1, no_of_matchweeks + 1):
                if matchweek not in fixture_table[team.assigned_index] and matchweek not in fixture_table[:, team.assigned_index]:
                    # If the matchweek is not found in home fixtures (row) or in away fixtures (column)
                    self.logger.debug(f'constraint violated from team with id {team.id} and assigned index {team.assigned_index} '
                                      f'matchweek {matchweek}')
                    return True

        return False
