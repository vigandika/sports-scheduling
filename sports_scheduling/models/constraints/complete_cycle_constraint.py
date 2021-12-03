from typing import List

from numpy import ndarray

from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team


class CompleteCycleConstraint(BaseConstraint):

    def __init__(self):
        """Each team should play once against each other team before playing a team for the second time"""
        super().__init__(bracket='completeCycleConstraint', level='HARD')

    def is_violated(self, teams: List[Team], fixture_table: ndarray) -> bool:
        first_half_season_matchweeks = [i for i in range(len(teams))]
        for team in teams:
            for i in range(len(teams)):
                if fixture_table[team.assigned_index, i] == 0:
                    continue

                if fixture_table[team.assigned_index, i] in first_half_season_matchweeks and \
                        fixture_table[i, team.assigned_index] in first_half_season_matchweeks:
                    # If a team plays twice against another team in the matchweeks of the first half of the season, it means a team has
                    # failed to meet every team in the first half of the season and has instead played twice against the same team.
                    return True

        return False
