from typing import List

from numpy import ndarray

from sports_scheduling.log import init_logging
from sports_scheduling.models.teams.teams import Team


class BaseConstraint:

    def __init__(self, bracket, level):
        self.logger = init_logging().getLogger(__name__)
        self.bracket = bracket
        self.level = level

    def is_violated(self, teams: List[Team], fixture_table: ndarray) -> bool:
        raise NotImplementedError()
