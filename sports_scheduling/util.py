import numpy as np
from numpy import ndarray


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