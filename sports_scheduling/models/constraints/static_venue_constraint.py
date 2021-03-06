import copy
from typing import List

from numpy import ndarray

from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team
from sports_scheduling.util import contains_n_consecutive_numbers


class StaticVenueConstraint(BaseConstraint):

    def __init__(self, maximum: int):
        """Limit the number of consecutive games a team can play in the same venue"""
        super().__init__(bracket='staticVenueConstraint', level='HARD')

        assert isinstance(maximum, int)
        self.maximum = maximum

    def is_violated(self, teams: List[Team], fixture_table: ndarray) -> bool:
        schedule_table = copy.deepcopy(fixture_table)
        for home_fixture_list in schedule_table:
            # Remove zeros
            matchweeks = [matchweek for matchweek in home_fixture_list if matchweek != 0]
            if contains_n_consecutive_numbers(matchweeks, self.maximum + 1):
                return True

        # Iterate away fixtures in the transposed matrix
        for away_fixture_list in schedule_table.T:
            # Remove zeros
            matchweeks = [matchweek for matchweek in away_fixture_list if matchweek != 0]
            if contains_n_consecutive_numbers(matchweeks, self.maximum + 1):
                return True

        return False
