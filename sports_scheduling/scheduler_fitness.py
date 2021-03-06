from typing import List

from numpy import ndarray

from sports_scheduling.log import get_logger
from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team


class SchedulerFitness:

    def __init__(self, hard_constraints: List[BaseConstraint], soft_constraints: List[BaseConstraint]):
        self.logger = get_logger(__name__)
        self.hard_constraints = hard_constraints
        self.soft_constraints = soft_constraints

    def is_feasible_solution(self, fixture_table: ndarray, teams: List[Team]) -> bool:
        """Check if any of the hard constraints is violated."""
        for constraint in self.hard_constraints:
            if constraint.is_violated(teams, fixture_table):
                self.logger.debug(f'hard constraint not satisfied {vars(constraint)}\n')
                return False

        return True

    def get_fitness_value(self, fixture_table: ndarray, teams: List[Team]) -> int:
        """Calculate the fitness of a solution by checking how many soft constraints have been violated."""
        total_penalty_score = 0
        for constraint in self.soft_constraints:
            assert (penalty := getattr(constraint, 'penalty')) is not None, f'penalty attr missing for soft constraint {constraint.bracket}'
            if constraint.is_violated(teams, fixture_table):
                self.logger.debug(f'violated soft constraint: {vars(constraint)}')
                total_penalty_score += penalty
            else:
                self.logger.debug(f'didnt violate soft constraint: {vars(constraint)}')

        return total_penalty_score
