import copy
import math
import random
from typing import List, Tuple

from numpy import ndarray

from sports_scheduling.log import get_logger
from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team
from sports_scheduling.operators import swap_homes, swap_schedules, swap_matchweeks
from sports_scheduling.scheduler_fitness import SchedulerFitness


class SimulatedAnnealing:

    def __init__(self, hard_constraints: List[BaseConstraint], soft_constraints: List[BaseConstraint]):
        self.logger = get_logger(__name__)
        self.fitness = SchedulerFitness(hard_constraints, soft_constraints)

    def run(self, initial_state: ndarray, teams: List[Team]):
        # initial_temperature = config['simulated_annealing']['initial_temp']
        # cooling_rate = config['simulated_annealing']['cooling_rate']
        #
        initial_temp = 90
        final_temp = .1
        alpha = 0.01

        current_temp = initial_temp
        # Start by initializing the current state with the initial state
        current_state = initial_state
        current_teams = teams

        self.logger.info(f'current fitness: {self.fitness.get_fitness_value(current_state, current_teams)}')
        while current_temp > final_temp:
            neighbor_state, neighbor_teams = self.get_random_neighbor(current_state, current_teams)
            # Check if neighbor is a feasible solution
            if self.fitness.is_feasible_solution(neighbor_state, neighbor_teams):
                # Check if neighbor is a better solution
                # Lower fitness value better solution
                fitness_diff = self.fitness.get_fitness_value(current_state, current_teams) - \
                               self.fitness.get_fitness_value(neighbor_state, neighbor_teams)

                # if the new solution is better, accept it
                if fitness_diff > 0:
                    self.logger.info(f'accepting state with fitness: {self.fitness.get_fitness_value(neighbor_state, neighbor_teams)}')
                    current_state, current_teams = neighbor_state, neighbor_teams
                # if the new solution is not better, accept it with a probability of e^(-cost/temp)
                else:
                    if random.uniform(0, 1) < math.exp(fitness_diff / current_temp):
                        self.logger.info(f'accepting state with fitness: {self.fitness.get_fitness_value(neighbor_state, neighbor_teams)}')
                        current_state, current_teams = neighbor_state, neighbor_teams

                # decrement the temperature
                current_temp -= alpha

        self.logger.info(f'final fitness: {self.fitness.get_fitness_value(current_state, current_teams)}')
        return current_state, current_teams

    def get_random_neighbor(self, state: ndarray, teams: List[Team]) -> Tuple[ndarray, List[Team]]:
        operators = ['swap_homes', 'swap_schedules', 'swap_matchweeks']
        random_operator = random.choice(operators)
        tentative_teams = copy.deepcopy(teams)

        if random_operator == 'swap_homes':
            return swap_homes(state, self.get_random_team(tentative_teams), self.get_random_team(tentative_teams)), tentative_teams

        elif random_operator == 'swap_schedules':
            swap_schedules(self.get_random_team(tentative_teams), self.get_random_team(tentative_teams))
            return state, tentative_teams

        elif random_operator == 'swap_matchweeks':
            no_of_teams = len(tentative_teams)
            return swap_matchweeks(state, self.get_random_matchweek(no_of_teams), self.get_random_matchweek(no_of_teams)), tentative_teams

    @staticmethod
    def get_random_team(teams: List[Team]) -> Team:
        return random.choice(teams)

    @staticmethod
    def get_random_matchweek(no_of_teams: int) -> int:
        return random.choice([matchweek + 1 for matchweek in range((no_of_teams - 1) * 2)])
