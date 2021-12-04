from pprint import pprint
from typing import List

from numpy import ndarray

from sports_scheduling.log import init_logging
from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team


class SchedulerFitness:

    def __init__(self, teams: List[Team], hard_constraints: List[BaseConstraint], soft_constraints: List[BaseConstraint]):
        self.logger = init_logging().getLogger(__name__)
        self.teams = teams
        self.hard_constraints = hard_constraints
        self.soft_constraints = soft_constraints

    def is_feasible_solution(self, fixture_table: ndarray) -> bool:
        """Check if any of the hard constraints is violated."""
        for constraint in self.hard_constraints:
            if constraint.is_violated(self.teams, fixture_table):
                self.logger.error(f'hard constraint not satisfied {vars(constraint)}\n')
                return False

        return True

    def get_fitness_value(self, fixture_table: ndarray) -> int:
        """Calculate the fitness of a solution by checking how many soft constraints have been violated."""
        total_penalty_score = 0
        for constraint in self.soft_constraints:
            assert (penalty := getattr(constraint, 'penalty')) is not None, f'penalty attr missing for soft constraint {constraint.bracket}'
            if constraint.is_violated(self.teams, fixture_table):
                self.logger.debug(f'violated soft constraint: {vars(constraint)}')
                total_penalty_score += penalty

        return total_penalty_score
