import copy
from itertools import groupby
from operator import itemgetter
from typing import List

from numpy import ndarray

from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team


class StaticVenueConstraint(BaseConstraint):

    def __init__(self, maximum: int):
        """Limit the number of consecutive games a team can play in the same venue"""
        super().__init__(bracket='staticVenueConstraint', level='HARD')
        self.maximum = maximum

    def is_violated(self, teams: List[Team], fixture_table: ndarray) -> bool:
        schedule_table = copy.deepcopy(fixture_table)
        for home_fixture_list in schedule_table:
            # Remove zeros
            matchweeks = [matchweek for matchweek in home_fixture_list if matchweek != 0]
            matchweeks.sort()
            for k, g in groupby(enumerate(home_fixture_list), lambda x: x[0] - x[1]):
                group = (map(itemgetter(1), g))
                group = list(map(int, group))

                if len(group) > self.maximum:
                    return True

        for away_fixture_list in schedule_table.T:
            # Remove zeros
            matchweeks = [matchweek for matchweek in away_fixture_list if matchweek != 0]
            matchweeks.sort()
            for k, g in groupby(enumerate(away_fixture_list), lambda x: x[0] - x[1]):
                group = (map(itemgetter(1), g))
                group = list(map(int, group))

                if len(group) > self.maximum:
                    return True

        return False

