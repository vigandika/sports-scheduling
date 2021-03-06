import random
from itertools import groupby
from operator import itemgetter
from typing import List, Tuple, Dict

import numpy as np
from numpy import ndarray

from sports_scheduling.log import get_logger
from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team

logger = get_logger(__name__)


def get_team_by_id(teams: List[Team], id: int) -> Team:
    """Get team from the set of ``teams`` received as argument matched with ``id``."""
    for team in teams:
        if team.id == id:
            return team
    raise LookupError(f'could not find team with id {id} in teams {teams}')


__team_id_mapping = {}


def get_unchanged_team_by_id(team_id: int) -> Team:
    """
    Get `team` by id leveraging a stored mapping.

    The class :attr:``__team_id_mapping`` mapping is created during the parsing of the data and is unchanged afterwards.

    The method is a more convenient option to get a team by its id than `get_team_by_id` as it makes use of a stored mapping instead of
    having to iterate over a list and compare the id properties. Should be used when static properties of a team are of interest, like
    ``name`` and ``category``. Since the mapping does not change after first being populated this method should not be used when wanting
    to use dynamic properties of a team, like ``assigned_index``.
    """
    assert __team_id_mapping, 'team_id_mapping is accessed but it\'s empty'
    return __team_id_mapping[team_id]


def get_team_by_index(teams: List[Team], index: int) -> Team:
    """Get team from the set of ``teams`` received as argument matched with ``index``."""
    for team in teams:
        if team.assigned_index == index:
            return team
    raise LookupError(f'could not find team with id {index} in teams {teams}')


def contains_n_consecutive_numbers(numbers_list: List[int], number_of_consecutive_values: int):
    """
    TODO
    :param numbers_list:
    :param number_of_consecutive_values:
    :return:
    """
    numbers_list.sort()
    for k, g in groupby(enumerate(numbers_list), lambda x: x[0] - x[1]):
        group = (map(itemgetter(1), g))
        group = list(map(int, group))

        if len(group) >= number_of_consecutive_values:
            return True
    return False


def assign_teams(teams: List[Team], shared_venue_team_pairs: List[Tuple[int, int]], indexes_of_shared_venue_teams: List[Tuple[int, int]]):
    """
    TODO
    :param teams:
    :param shared_venue_team_pairs:
    :param indexes_of_shared_venue_teams:
    :return:
    """
    available_indexes = [i for i in range(len(teams))]
    number_of_shared_venue_team_pairs = len(shared_venue_team_pairs)
    # assign shared venue teams first if there are any
    if number_of_shared_venue_team_pairs > 0:
        assert indexes_of_shared_venue_teams, 'shared venue teams applicable but indexes are not specified'
        for index, pair in enumerate(shared_venue_team_pairs):
            logger.info(f'setting shared venue teams with IDs: {shared_venue_team_pairs} indexes {indexes_of_shared_venue_teams}')

            # First element of the pair
            team = get_team_by_id(teams, pair[0])
            index_to_assign = indexes_of_shared_venue_teams[index][0]
            __assign_team_to_index(team, index_to_assign)
            available_indexes.remove(index_to_assign)

            # Second element of the pair
            team = get_team_by_id(teams, pair[1])
            index_to_assign = indexes_of_shared_venue_teams[index][1]
            __assign_team_to_index(team, index_to_assign)
            available_indexes.remove(index_to_assign)

    for team in teams:
        # Randomly set other indexes
        if team.assigned_index is None:
            random_index = random.choice(available_indexes)
            __assign_team_to_index(team, random_index)
            available_indexes.remove(random_index)


def __assign_team_to_index(team: Team, index_to_assign: int):
    logger.debug(f'setting index {index_to_assign} to team with ID {team.id}')
    team.assigned_index = index_to_assign


def get_solution_response(fixture_table: ndarray, teams: List[Team]):
    team_index_mapping: Dict[int, Team] = {}
    for team in teams:
        team_index_mapping[team.assigned_index] = team

    no_of_games_per_round = len(fixture_table) // 2
    response_dict = {'matchweeks': []}
    for matchweek in range((len(fixture_table) - 1) * 2):
        # get coordinates ((x1,x2,xn...), (y1,y2,yn...)) where condition
        matchweek_coordinates = np.where(fixture_table == matchweek + 1)

        matchweek_fixtures = {"fixtures": []}
        for game in range(no_of_games_per_round):
            matchweek_fixtures["fixtures"].append({
                "homeTeam": team_index_mapping[matchweek_coordinates[0][game]].name,
                "awayTeam": team_index_mapping[matchweek_coordinates[1][game]].name
            })
        response_dict['matchweeks'].append(matchweek_fixtures)

    return response_dict


def parse_data(data: dict) -> Tuple[List[Team], List[BaseConstraint], List[BaseConstraint]]:
    from sports_scheduling.models.constraints import CompleteCycleConstraint, EncounterConstraint, ParticipationConstraint, \
        StaticVenueConstraint, SharedVenueConstraint, OpponentConstraint, VenueConstraint, RepeaterGapConstraint, FairnessConstraint

    teams: List[Team] = []
    soft_constraints: List[BaseConstraint] = []
    hard_constraints: List[BaseConstraint] = []

    if len(data.get("teams")) < 5:
        raise ValueError('the number of teams should be at least 5')

    try:
        for team in data["teams"]:
            team_obj = Team(id=team['id'], name=team['name'], category=team.get('category'))
            teams.append(team_obj)
            __team_id_mapping[team['id']] = team_obj
        if len(teams) % 2 != 0:
            # If the number of teams is odd, add team indicating a bye (https://en.wikipedia.org/wiki/Bye_(sports))
            teams.append(Team(0, 'bye', None))

    except Exception:
        raise RuntimeError(f"an expected error occurred when processing teams in data {data}")

    try:
        for constraint in data['constraints']:
            if constraint['level'] == 'HARD':
                if constraint['type'] == 'completeCycleConstraint':
                    hard_constraints.append(CompleteCycleConstraint())
                elif constraint['type'] == 'encounterConstraint':
                    hard_constraints.append(EncounterConstraint())
                elif constraint['type'] == 'participationConstraint':
                    hard_constraints.append(ParticipationConstraint())
                elif constraint['type'] == 'staticVenueConstraint':
                    hard_constraints.append(StaticVenueConstraint(maximum=constraint['maximum']))
                elif constraint['type'] == 'sharedVenueConstraint':
                    hard_constraints.append(SharedVenueConstraint(shared_venue_team_pairs=constraint['teamPairs']))
                else:
                    raise ValueError(f"unrecognized hard constraint type '{constraint['type']}'")

            elif constraint['level'] == 'SOFT':
                if constraint['type'] == 'opponentConstraint':
                    soft_constraints.append(
                        OpponentConstraint(
                            team_id=constraint['teamId'],
                            opponent_id=constraint['opponentId'],
                            matchweek=constraint['matchweek'],
                            penalty=constraint['penalty'],
                        )
                    )
                elif constraint['type'] == 'venueConstraint':
                    soft_constraints.append(
                        VenueConstraint(
                            team_id=constraint['teamId'],
                            venue=constraint['venue'],
                            matchweek=constraint['matchweek'],
                            penalty=constraint['penalty'],
                        )
                    )
                elif constraint['type'] == 'repeaterGapConstraint':
                    soft_constraints.append(
                        RepeaterGapConstraint(
                            team1_id=constraint['team1Id'],
                            team2_id=constraint['team2Id'],
                            minimum_gap=constraint['minimumGap'],
                            penalty=constraint['penalty'],
                        )
                    )
                elif constraint['type'] == 'fairnessConstraint':
                    soft_constraints.append(
                        FairnessConstraint(
                            consecutive_hard_matches=constraint['consecutiveHardMatches'],
                            penalty=constraint['penalty'],
                        )
                    )
                else:
                    raise ValueError(f"unrecognized soft constraint type '{constraint['type']}'")
            else:
                raise ValueError(f"unrecognized level type '{constraint['type']}'")
    except Exception:
        raise RuntimeError(f"an expected error occurred when processing constraints in data {data}")

    return teams, hard_constraints, soft_constraints


def print_fixture_list(fixture_table: ndarray, teams: List[Team]):
    # Create team index mapping to avoid overusing of a potential get_team_by_index method
    team_index_mapping: Dict[int, Team] = {}
    for team in teams:
        team_index_mapping[team.assigned_index] = team

    no_of_games_per_round = len(fixture_table) // 2
    for matchweek in range((len(fixture_table) - 1) * 2):
        # get coordinates ((x1,x2,xn...), (y1,y2,yn...)) where condition
        matchweek_coordinates = np.where(fixture_table == matchweek + 1)
        matchweek_fixtures = f"""
            MATCHWEEK {matchweek + 1}:
        """
        for game in range(no_of_games_per_round):
            matchweek_fixtures = f"{matchweek_fixtures}\n\t\t{team_index_mapping[matchweek_coordinates[0][game]].name} - " \
                                 f"{team_index_mapping[matchweek_coordinates[1][game]].name}"

        print(matchweek_fixtures)
