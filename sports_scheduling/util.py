import math
import random
from typing import List, Tuple, Optional, Dict

import numpy as np
from numpy import ndarray

from sports_scheduling.log import get_logger
from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team

logger = get_logger(__name__)


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


def get_solution_response(fixture_table: ndarray, teams: List[Team]):
    team_index_mapping: Dict[int, Team] = {}
    for team in teams:
        team_index_mapping[team.assigned_index] = team

    no_of_games_per_round = len(fixture_table) // 2
    response_dict = {}
    for matchweek in range((len(fixture_table) - 1) * 2):
        # get coordinates ((x1,x2,xn...), (y1,y2,yn...)) where condition
        matchweek_coordinates = np.where(fixture_table == matchweek + 1)
        matchweek_fixtures = f"""
            MATCHWEEK {matchweek + 1}:
        """
        response_dict[f"matchweek_{matchweek + 1}"] = []
        for game in range(no_of_games_per_round):
            response_dict[f"matchweek_{matchweek + 1}"].append({
                "homeTeam": team_index_mapping[matchweek_coordinates[0][game]].name,
                "awayTeam": team_index_mapping[matchweek_coordinates[1][game]].name
            })

    return response_dict


def parse_data(data: dict) -> Tuple[List[Team], List[BaseConstraint], List[BaseConstraint]]:
    from sports_scheduling.models.constraints import CompleteCycleConstraint, EncounterConstraint, ParticipationConstraint, \
        StaticVenueConstraint, SharedVenueConstraint, OpponentConstraint, VenueConstraint, RepeaterGapConstraint, FairnessConstraint

    teams: List[Team] = []
    soft_constraints: List[BaseConstraint] = []
    hard_constraints: List[BaseConstraint] = []

    try:
        for team in data["teams"]:
            teams.append(Team(id=team['id'], name=team['name'], category=team['category']))
    except Exception:
        raise RuntimeError(f"an expected error occurred when processing team {team} in data {data}")

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
                    hard_constraints.append(SharedVenueConstraint(shared_venue_team_pairs=constraint['teams']))
                else:
                    raise TypeError(f"unrecognized hard constraint type '{constraint['type']}'")

            elif constraint['level'] == 'SOFT':
                if constraint['type'] == 'opponentConstraint':
                    soft_constraints.append(OpponentConstraint(team_id=constraint['teamId'], opponent_id=constraint['opponentId'],
                                                               matchweek=constraint['matchweek'], penalty=constraint['penalty']))
                elif constraint['type'] == 'venueConstraint':
                    soft_constraints.append(VenueConstraint(team_id=constraint['teamId'], venue=constraint['venue'],
                                                            matchweek=constraint['matchweek'], penalty=constraint['penalty']))
                elif constraint['type'] == 'repeaterGapConstraint':
                    soft_constraints.append(RepeaterGapConstraint(team1_id=constraint['team1Id'], team2_id=constraint['team2Id'],
                                                                  minimum_gap=constraint['minimumGap'], penalty=constraint['penalty']))
                elif constraint['type'] == 'fairnessConstraint':
                    soft_constraints.append(FairnessConstraint(consecutive_hard_matches=constraint['consecutiveHardMatches']))
                else:
                    raise TypeError(f"unrecognized soft constraint type '{constraint['type']}'")
            else:
                raise TypeError(f"unrecognized level type '{constraint['type']}'")
    except Exception:
        raise RuntimeError(f"an expected error occurred when processing constraint {constraint} in data {data}")

    return teams, hard_constraints, soft_constraints
