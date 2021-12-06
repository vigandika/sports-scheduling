from typing import List

from numpy import ndarray

from sports_scheduling.config.config import config
from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team


class SimulatedAnnealing:

    @staticmethod
    def solve(initial_solution: ndarray, teams: List[Team], hard_constraints: List[BaseConstraint], soft_constraints: List[BaseConstraint]):
        initial_temperature = config['simulated_annealing']['initial_temp']
        cooling_rate = config['simulated_annealing']['cooling_rate']
