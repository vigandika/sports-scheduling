import numpy as np
from numpy import ndarray


def generate_initial_solution(number_of_teams: int):
    fixture_table = np.zeros((number_of_teams, number_of_teams), dtype='int')
    get_berger_table(number_of_teams, fixture_table)
    return
    for i in range(number_of_teams - 1):
        fill = True if i % 2 != 0 else False
        for j in range(number_of_teams - 1):
            if i == j:
                # Always fill the diagonal
                fixture_table[i, j] = i + 1
            print(fixture_table[i, j])

    print(fixture_table)


def get_berger_table(n: int, matrix: ndarray):
    # n - number of teams
    n = n - 1  # because berger
    for i in range(n):
        round = i + 1
        for j in range(n):
            matrix[i, j] = round
            round += 1
            if round > n:
                round = 1

    print(matrix)


generate_initial_solution(4)
