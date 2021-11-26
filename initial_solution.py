import numpy as np
from numpy import ndarray


def generate_initial_solution(number_of_teams: int):
    fixture_table = np.zeros((number_of_teams, number_of_teams), dtype='int')
    get_balanced_berger_table(number_of_teams, fixture_table)
    return
    for i in range(number_of_teams - 1):
        fill = True if i % 2 != 0 else False
        for j in range(number_of_teams - 1):
            if i == j:
                # Always fill the diagonal
                fixture_table[i, j] = i + 1
            print(fixture_table[i, j])

    print(fixture_table)


def get_balanced_berger_table(n: int, matrix: ndarray):
    # n - number of teams
    n = n - 1  # because berger
    for i in range(n):
        assign_as_reverse_fixture = False if i % 2 == 0 else True
        match_week = i + 1
        for j in range(n):
            if matrix[i, j] != 0:
                # If it's already assigned just increase the match_week
                match_week += 1
                if match_week > n:
                    match_week = 1
                assign_as_reverse_fixture = not assign_as_reverse_fixture
                continue
            # Decide whether it's first or second fixture
            if i == j:
                # Always fill diagonal
                matrix[i, j] = match_week
                match_week += 1
                if match_week > n:
                    match_week = 1
                continue
            elif assign_as_reverse_fixture:
                matrix[i, j] = match_week + n
                # Set reverse fixture to the reflection against the diagonal
                matrix[j, i] = match_week
            else:
                matrix[i, j] = match_week
                matrix[j, i] = match_week + n

            assign_as_reverse_fixture = not assign_as_reverse_fixture

            match_week += 1
            if match_week > n:
                match_week = 1

    print(matrix)


generate_initial_solution(6)
