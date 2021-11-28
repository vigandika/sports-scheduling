import math
from itertools import groupby
from operator import itemgetter
from typing import List, Optional

import numpy as np
from numpy import ndarray

from sports_scheduling.log import init_logging


class Scheduler:

    def __init__(self, number_of_teams: int, number_of_shared_venue_pairs: int):
        # init logging
        self.logger = init_logging().getLogger(__name__)
        self.number_of_teams = number_of_teams
        self.number_of_shared_venue_pairs = number_of_shared_venue_pairs
        self.fixture_table = np.zeros((number_of_teams, number_of_teams), dtype='int')

    def generate(self):
        self.fill_balanced_bergers_table()
        self.assign_last_team_matches()

    def fill_balanced_bergers_table(self):
        n = self.number_of_teams - 1  # because bergers wants n-1

        for i in range(n):
            assign_as_reverse_fixture = False if i % 2 == 0 else True
            match_week = i + 1
            for j in range(n):
                if self.fixture_table[i, j] != 0:
                    # If it's already assigned just increase the match_week
                    match_week += 1
                    if match_week > n:
                        match_week = 1
                    assign_as_reverse_fixture = not assign_as_reverse_fixture
                    continue
                # Decide whether it's first or second fixture
                if i == j:
                    # Always fill diagonal
                    self.fixture_table[i, j] = match_week
                    match_week += 1
                    if match_week > n:
                        match_week = 1
                    continue
                elif assign_as_reverse_fixture:
                    self.fixture_table[i, j] = match_week + n
                    # Set reverse fixture to the reflection against the diagonal
                    self.fixture_table[j, i] = match_week
                else:
                    self.fixture_table[i, j] = match_week
                    self.fixture_table[j, i] = match_week + n

                assign_as_reverse_fixture = not assign_as_reverse_fixture

                match_week += 1
                if match_week > n:
                    match_week = 1

    def assign_last_team_matches(self):
        """
        The given table is the fixture table but without the matches of the n-th team determined.
        In first look, it also contains hard constraint violations because:
            1. shared venue teams play at the same venue in some match_weeks
            2. some teams play more than 2 straight games in the same venue

        If we look closely, these violations occur only in the diagonal matchweeks - where teams play against each other.
        The match-week where the team plays against itself (diagonal) actaully represent games that team plays against
        the n-th team not included in the table yet

        This method assign the opponents to the nth team, while being careful to respect the above mentioned 2 hard
        constraints mentioned above

        Identify the shared venue teams. Naturally, the teams with the schedules becoming closest to being opposites (when
        one plays A the other plays H and Vice versa) are the teams
            * 1 and x where x is n/2 (if even) n/2 + 1 (if odd)
            if n is 10:
            1 and 5
        # Get indexes of shared venue teams
        indexes_of_shared_venue_teams = [(i, math.ceil(no_of_teams / 2 + i - 1)) for i in range(number_of_shared_venue_pairs)]
            2 and 6
            3 and 7
            ...

        The maximum number of shared Venue teams that result with n-teams competitions is TODO
        """
        # Transfer match-weeks from diagonal to the n-th column (filled with zeros at the moment)
        # print(fixture_table)

        no_of_teams = len(self.fixture_table)
        self.logger.info(f'number of teams is {no_of_teams}')
        n = no_of_teams - 1

        # Get indexes of shared venue teams
        indexes_of_shared_venue_teams = [(i, math.ceil(no_of_teams / 2 + i - 1)) for i in range(self.number_of_shared_venue_pairs)]
        self.logger.info(f'shared venue team indexes out of {no_of_teams} are {indexes_of_shared_venue_teams}'
                         f'(human readable: {[(x + 1, y + 1) for x, y in indexes_of_shared_venue_teams]})')

        # Avoid modifying the object
        diagonal_values = self.fixture_table.diagonal().copy()

        # Before checking hard constraints make sure diagonal is set to zero so hard constraints violated by the diagonal are disregarded
        np.fill_diagonal(self.fixture_table, np.zeros(self.number_of_shared_venue_pairs, dtype='int'))

        # Shared value teams will have only one conflict and it's the game in the lower index's diagonal
        # Change that to the match_week to be played in the second half of the season (reflection + n)
        for team_pair in indexes_of_shared_venue_teams:
            # Get match week which we can set in the n-th col

            valid_game_week = self.check_hard_constraints(
                tentative_values=[diagonal_values[team_pair[0]], diagonal_values[team_pair[0]] + n],
                row=team_pair[0],
                col=n,
                fixture_table=self.fixture_table,
                complementary_team=team_pair[1]
            )

            self.logger.debug(f'setting {team_pair[0]} up against n-th team at Home in match week {valid_game_week}')
            if valid_game_week <= n:
                # If the valid game week is less then n it means the first half of the season. Assign the match week and then its reflection
                # (second half of the season)
                self.fixture_table[team_pair[0], n] = valid_game_week
                self.fixture_table[n, team_pair[0]] = valid_game_week + n
            else:
                # Else, reverse
                self.fixture_table[team_pair[0], n] = valid_game_week
                self.fixture_table[n, team_pair[0]] = valid_game_week - n

            valid_game_week = self.check_hard_constraints(
                tentative_values=[diagonal_values[team_pair[1]], diagonal_values[team_pair[1]] + n],
                row=team_pair[1],
                col=n,
                fixture_table=self.fixture_table,
                complementary_team=team_pair[0],
            )

            self.logger.debug(f'setting {team_pair[1]} up against n-th team at Home in match week {valid_game_week}')
            if valid_game_week <= n:
                self.fixture_table[team_pair[1], n] = valid_game_week
                self.fixture_table[n, team_pair[1]] = valid_game_week + n
            else:
                self.fixture_table[team_pair[1], n] = valid_game_week
                self.fixture_table[n, team_pair[1]] = valid_game_week - n

        # Fill out remaining matches
        for i in range(no_of_teams):
            if i == n:
                # If last row and last column is reached (should be zero) the fixture is complete
                break
            if self.fixture_table[i][n] != 0:
                # Skip already assigned matchweeks
                continue

            valid_game_week = self.check_hard_constraints([diagonal_values[i], diagonal_values[i] + n], i, n, self.fixture_table)
            if valid_game_week <= n:
                self.fixture_table[i, n] = valid_game_week
                self.fixture_table[n, i] = valid_game_week + n
            else:
                self.fixture_table[i, n] = valid_game_week
                self.fixture_table[n, i] = valid_game_week - n

    def check_hard_constraints(self, tentative_values: List[int], row: int, col: int, fixture_table: ndarray,
                               complementary_team: int = None):

        self.logger.debug(f'attempting to place match week(s) {tentative_values} in position ({row}, {col})'
                          f' in fixture table\n{fixture_table}')

        for tentative_value in tentative_values:
            # Check that the home team (row) does not already play at Home in the game week tentative_val
            if tentative_value in fixture_table[row]:
                continue

            # Check that away team (column) does not play away in the same game week tentative_val
            if tentative_value in fixture_table[:, col]:
                continue

            # Check that the complementary_team does not play in the same venue at Home in the match week (which means it plays away)
            if complementary_team is not None and tentative_value in fixture_table[complementary_team]:
                continue

            # Check that no 3 consecutive values are in home games (row)
            if self.find_n_consecutive_values(3, fixture_table[row], tentative_value) is True:
                continue

            # Check that not 3 consecutive values are in away games (col)
            if self.find_n_consecutive_values(3, fixture_table[:, col], tentative_value) is True:
                continue

            return tentative_value

        self.logger.warning(f'could not add any of the tentative value {tentative_values} in {fixture_table}')
        return None

    @staticmethod
    def find_n_consecutive_values(n: int, team_fixture_list: ndarray, tentative_value: Optional[int] = None):
        """
        https://stackoverflow.com/a/2154437
        """
        fixture_list = team_fixture_list.copy()
        fixture_list = fixture_list.tolist()
        if tentative_value:
            fixture_list.append(tentative_value)

        # Remove zeros
        fixture_list = [match_week for match_week in fixture_list if match_week != 0]
        fixture_list.sort()
        for k, g in groupby(enumerate(fixture_list), lambda x: x[0] - x[1]):
            group = (map(itemgetter(1), g))
            group = list(map(int, group))

            if len(group) >= n:
                return True

        return False
