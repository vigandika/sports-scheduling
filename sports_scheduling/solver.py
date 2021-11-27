import numpy as np

from log import init_logging



class Solver:

    def __init__(self, number_of_teams: int, number_of_shared_venue_pairs: int):
        # init logging
        self.logger = init_logging()
        self.logger.info('s')
        self.number_of_teams = number_of_teams
        self.number_of_shared_venue_teams = number_of_shared_venue_pairs
        self.fixture_table = np.zeros((number_of_teams, number_of_teams), dtype='int')

    def solve(self):
        self.fill_balanced_bergers_table()

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

a = Solver(10, 3)

    # def assign_last_team_matches(fixture_table: ndarray, number_of_shared_venue_pairs: int):
    #     """
    #     The given table is the fixture table but without the matches of the n-th team determined.
    #     In first look, it also contains hard constraint violations because:
    #         1. shared venue teams play at the same venue in some match_weeks
    #         2. some teams play more than 2 straight games in the same venue
    #
    #     If we look closely, these violations occur only in the diagonal matchweeks - where teams play against each other.
    #     The match-week where the team plays against itself (diagonal) actaully represent games that team plays against
    #     the n-th team not included in the table yet
    #
    #     This method assign the opponents to the nth team, while being careful to respect the above mentioned 2 hard
    #     constraints mentioned above
    #
    #     Identify the shared venue teams. Naturally, the teams with the schedules becoming closest to being opposites (when
    #     one plays A the other plays H and Vice versa) are the teams
    #         * 1 and x where x is n/2 (if even) n/2 + 1 (if odd)
    #         if n is 10:
    #         1 and 5
    #         2 and 6
    #         3 and 7
    #         ...
    #
    #     The maximum number of shared Venue teams that result with n-teams competitions is TODO
    #     """
    #     # Transfer match-weeks from diagonal to the n-th column (filled with zeros at the moment)
    #     # print(fixture_table)
    #
    #     no_of_teams = len(fixture_table)
    #     logger.info(f'number of teams is {no_of_teams}')
    #     n = len(fixture_table) - 1
    #     # Get indexes of shared venue teams
    #     indexes_of_shared_venue_teams = [(i, math.ceil(no_of_teams / 2 + i - 1)) for i in range(number_of_shared_venue_pairs)]
    #     logger.info(f'shared venue team indexes out of {no_of_teams} are {indexes_of_shared_venue_teams}\n'
    #                 f'human readable: {[(x + 1, y + 1) for x, y in indexes_of_shared_venue_teams]}')
    #
    #     # Avoid modifying the object
    #     diagonal_values = fixture_table.diagonal().copy()
    #
    #     # Before checking hard constraints make sure diagonal is set to zero so hard constraints violated by the diagonal are disregarded
    #     np.fill_diagonal(fixture_table, np.zeros(number_of_shared_venue_pairs, dtype='int'))
    #
    #     # Shared value teams will have only one conflict and it's the game in the lower index's diagonal
    #     # Change that to the match_week to be played in the second half of the season (reflection + n)
    #     for team_pair in indexes_of_shared_venue_teams:
    #         # Get match week which we can set in the n-th col
    #
    #         valid_game_week = check_hard_constraints(
    #             tentative_values=[diagonal_values[team_pair[0]], diagonal_values[team_pair[0]] + n],
    #             row=team_pair[0],
    #             col=n,
    #             fixture_table=fixture_table,
    #             complementary_team=team_pair[1]
    #         )
    #
    #         logger.debug(f'setting {team_pair[0]} up against n-th team at Home in match week {valid_game_week}')
    #         if valid_game_week <= n:
    #             # If the valid game week is less then n it means the first half of the season. Assign the match week and then its reflection
    #             # (second half of the season)
    #             fixture_table[team_pair[0], n] = valid_game_week
    #             fixture_table[n, team_pair[0]] = valid_game_week + n
    #         else:
    #             # Else, reverse
    #             fixture_table[team_pair[0], n] = valid_game_week
    #             fixture_table[n, team_pair[0]] = valid_game_week - n
    #
    #         valid_game_week = check_hard_constraints(
    #             tentative_values=[diagonal_values[team_pair[1]], diagonal_values[team_pair[1]] + n],
    #             row=team_pair[1],
    #             col=n,
    #             fixture_table=fixture_table,
    #             complementary_team=team_pair[0],
    #         )
    #
    #         logger.debug(f'setting {team_pair[1]} up against n-th team at Home in match week {valid_game_week}')
    #         if valid_game_week <= n:
    #             fixture_table[team_pair[1], n] = valid_game_week
    #             fixture_table[n, team_pair[1]] = valid_game_week + n
    #         else:
    #             fixture_table[team_pair[1], n] = valid_game_week
    #             fixture_table[n, team_pair[1]] = valid_game_week - n
    #
    #     # Fill out remaining matches
    #     for i in range(no_of_teams):
    #         if i == n:
    #             # If last row and last column is reached (should be zero) the fixture is complete
    #             break
    #         if fixture_table[i][n] != 0:
    #             # Skip already assigned matchweeks
    #             continue
    #
    #         valid_game_week = check_hard_constraints([diagonal_values[i], diagonal_values[i] + n], i, n, fixture_table)
    #         if valid_game_week <= n:
    #             fixture_table[i, n] = valid_game_week
    #             fixture_table[n, i] = valid_game_week + n
    #         else:
    #             fixture_table[i, n] = valid_game_week
    #             fixture_table[n, i] = valid_game_week - n
