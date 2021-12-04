import copy

from numpy import ndarray

from sports_scheduling.models.teams.teams import Team


def swap_homes(fixture_table: ndarray, team_1: Team, team_2: Team) -> ndarray:
    """Return the mutated fixture table by switching the venues in matches between two teams"""
    # avoid modifying the object to avoid unexpected behavior
    schedule_table = copy.deepcopy(fixture_table)
    assert getattr(team_1, 'assigned_index') is not None and getattr(team_2, 'assigned_index') is not None, \
        f"either team with id {team_1.id} or opponent with id {team_2.id} have no assigned_index property"

    schedule_table[team_1.assigned_index, team_2.assigned_index], schedule_table[team_2.assigned_index, team_1.assigned_index] = \
        schedule_table[team_2.assigned_index, team_1.assigned_index], schedule_table[team_1.assigned_index, team_2.assigned_index]

    return schedule_table


def swap_schedules(team_1: Team, team_2: Team):
    """
    Change whole schedules of two teams. After the operator is applied they both will play the matches meant for the other team in the same
    order
    """
    team_1.assigned_index, team_2.assigned_index = team_2.assigned_index, team_1.assigned_index


def swap_matchweeks(fixture_table: ndarray, matchweek_1: int, matchweek_2: int) -> ndarray:
    """
    Change all fixtures of one matchweek to another matchweek and vice-versa.
    """
    assert {matchweek_1, matchweek_2} <= {i + 1 for i in range(len(fixture_table) * 2)}, \
        f"one of matchweeks ({matchweek_1}, {matchweek_2}) outside of legal bounds 1-{len(fixture_table)}"

    # avoid modifying the object to avoid unexpected behavior
    schedule_table = copy.deepcopy(fixture_table)
    # Assign the original matchweek_1 values to -1 to differ from matchweek_2 cells that are to be mutated to matchweek_1
    schedule_table[schedule_table == matchweek_1] = - 1
    # Mutate matchweek_2 to matchweek_1
    schedule_table[schedule_table == matchweek_2] = matchweek_1
    # Change the original targeted matchweek_1 values (now -1) to matchweek_2
    schedule_table[schedule_table == -1] = matchweek_2
    return schedule_table
