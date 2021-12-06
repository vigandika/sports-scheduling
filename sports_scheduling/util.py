import logging
import math
import random
from typing import List, Tuple, Optional

import numpy as np
from numpy import ndarray

from sports_scheduling.models.teams.teams import Team

logger = logging.getLogger(__name__)


def show_fixture_list(fixture_table: ndarray):
    no_of_games_per_round = len(fixture_table) // 2
    for match_week in range((len(fixture_table) - 1) * 2):
        item_index = np.where(fixture_table == match_week + 1)
        match_week_fixtures = f"""
            MATCHWEEK {match_week + 1}:
        """

        for game in range(no_of_games_per_round):
            match_week_fixtures = f"{match_week_fixtures}\n\t\t\t\t{item_index[0][game] + 1} - {item_index[1][game] + 1}"

        print(match_week_fixtures)


def get_team_by_id(teams: List[Team], id: int) -> Team:
    for team in teams:
        if team.id == id:
            return team
    raise LookupError(f'could not find team with id {id} in teams {teams}')


indexes_of_shared_venue_teams: Optional[List[Tuple[int, int]]] = None


def get_indexes_of_shared_venue_teams(number_of_teams: int, number_of_shared_venue_team_pairs: int) -> List[Tuple[int, int]]:
    """
    Naturally, the teams with the schedules becoming closest to being opposites (when
        one plays A the other plays H and Vice versa) are the teams
            * 1 and x where x is n/2 (if even) n/2 + 1 (if odd)
            if n is 10:
            1 and 5
        # Get indexes of shared venue teams
        indexes_of_shared_venue_teams = [(i, math.ceil(no_of_teams / 2 + i - 1)) for i in range(number_of_shared_venue_pairs)]
            team 1 and 5 (index 0 and 4)
            2 and 6 (1 and 5)
            3 and 7 (2 and 6)
            ...
    The maximum number of shared Venue teams that result with n-teams competitions is TODO
    """
    global indexes_of_shared_venue_teams

    if indexes_of_shared_venue_teams is not None:
        return indexes_of_shared_venue_teams

    indexes_of_shared_venue_teams = [(i, math.ceil(number_of_teams / 2 + i - 1)) for i in range(number_of_shared_venue_team_pairs)]
    return indexes_of_shared_venue_teams


def assign_teams(teams: List[Team], shared_venue_team_pairs: List[Tuple[int, int]]):
    available_indexes = [i for i in range(len(teams))]
    global indexes_of_shared_venue_teams
    number_of_shared_venue_team_pairs = len(shared_venue_team_pairs)
    # assign shared venue teams first
    if number_of_shared_venue_team_pairs > 0:
        # If there are shared venue teams in the problem
        assert len(indexes_of_shared_venue_teams) > 0, 'shared venue teams applicable but indexes are not specified'
        for index, pair in enumerate(shared_venue_team_pairs):
            logger.info(f'setting shared venue teams with IDs: {shared_venue_team_pairs} indexes {indexes_of_shared_venue_teams}')

            team = get_team_by_id(teams, pair[0])
            logger.debug(f'setting index {indexes_of_shared_venue_teams[index][0]} to team with ID {team.id}')
            team.assigned_index = indexes_of_shared_venue_teams[index][0]
            available_indexes.remove(indexes_of_shared_venue_teams[index][0])

            team = get_team_by_id(teams, pair[1])
            logger.debug(f'setting index {indexes_of_shared_venue_teams[index][1]} to team with ID {team.id}')
            team.assigned_index = indexes_of_shared_venue_teams[index][1]
            available_indexes.remove(indexes_of_shared_venue_teams[index][1])

    for team in teams:
        # Randomly set other indexes
        if team.assigned_index is None:
            random_index = random.choice(available_indexes)
            logger.debug(f'setting index {random_index} to team with ID {team.id}')
            team.assigned_index = random_index
            available_indexes.remove(random_index)

    print([vars(team) for team in teams])
