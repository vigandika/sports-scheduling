import copy
import math
import random
import time
from typing import List, Tuple, Optional

from numpy import ndarray

from sports_scheduling.log import get_logger
from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team
from sports_scheduling.operators import swap_homes, swap_schedules, swap_matchweeks
from sports_scheduling.scheduler_fitness import SchedulerFitness


class SimulatedAnnealing:
    initial_temp = 10000
    final_temp = 0

    def __init__(self, hard_constraints: List[BaseConstraint], soft_constraints: List[BaseConstraint]):
        self.logger = get_logger(__name__)
        self.fitness = SchedulerFitness(hard_constraints, soft_constraints)

    def run(self, initial_state: ndarray, teams: List[Team], max_time: Optional[int] = 30):
        current_temp = self.initial_temp
        # Start by initializing the current state with the initial state
        current_state = initial_state
        current_teams = teams
        self.logger.info(f'starting fitness: {self.fitness.get_fitness_value(current_state, current_teams)}')

        # track time spent if time limit is given
        start_time = time.time()

        # reporting stats
        max_dif = 0

        iteration = 0
        while current_temp > self.final_temp:
            iteration += 1

            if max_time and time.time() > start_time + max_time:
                # Return if time has run out
                self.logger.info(
                    f'time ran out. best solution found for {max_time}s: {self.fitness.get_fitness_value(current_state, current_teams)}')
                return current_state, current_teams

            neighbor_state, neighbor_teams = self.get_random_neighbor(current_state, current_teams)
            # Check if neighbor is a feasible solution
            if self.fitness.is_feasible_solution(neighbor_state, neighbor_teams):
                neighbor_fitness = self.fitness.get_fitness_value(neighbor_state, neighbor_teams)

                if neighbor_fitness == 0:
                    self.logger.info(f'found best possible solution with fitness {neighbor_fitness}')
                    return neighbor_state, neighbor_teams

                # Check if neighbor is a better solution (minimisation problem -> lower fitness value means better solution)
                fitness_diff = self.fitness.get_fitness_value(current_state, current_teams) - neighbor_fitness
                if abs(fitness_diff) > max_dif:
                    self.logger.info(f'changing max dif from {max_dif} to {abs(fitness_diff)}')
                    max_dif = abs(fitness_diff)

                # if the new solution is better, accept it
                if fitness_diff >= 0:
                    self.logger.info(f'accepting state with fitness: {neighbor_fitness}, temp: {current_temp}')
                    current_state, current_teams = neighbor_state, neighbor_teams
                else:
                    # if the new solution is not better, accept it with a probability
                    if random.uniform(0, 1) < math.exp(fitness_diff / current_temp):
                        self.logger.info(f'accepting with fitness: {neighbor_fitness}, temp: {current_temp}')
                        current_state, current_teams = neighbor_state, neighbor_teams

            # cool the system
            # current_temp = current_temp - 0.8 # arithmetic
            # current_temp = self.initial_temp - 0.8 * iteration  # linear
            current_temp = current_temp * 0.997  # linear geometric
            # current_temp = self.initial_temp *  math.pow(0.8, iteration)  # exponential
            # current_temp = self.initial_temp * math.pow((1 - (iteration / 15000)), 4)  # polynomial -> se ki bo hala
            # current_temp = (0.999 * self.initial_temp) / math.log(1 + iteration) # logarithmic
            # current_temp = current_temp / (1 + 0.001 * current_temp) # slow coolness function (initial = 1)

        self.logger.info(f'0 temperature is reached. Finishing with fitness {self.fitness.get_fitness_value(current_state, current_teams)}')
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
