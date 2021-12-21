from unittest import TestCase
from unittest.mock import patch

import numpy as np

from sports_scheduling.models.constraints.fairness_constraint import FairnessConstraint
from sports_scheduling.models.teams.teams import Team


@patch('sports_scheduling.models.constraints.base_constraint.get_logger')
class FairnessConstraintTests(TestCase):
    def test_is_violated(self, _):
        teams = [
            Team(1, 'xyz', 'A'),
            Team(2, 'xyz', 'A'),
            Team(3, 'xyz', 'C'),
            Team(4, 'xyz', 'B'),
            Team(5, 'xyz', 'B'),
            Team(6, 'xyz', 'B'),
        ]

        for index in range(len(teams)):
            teams[index].assigned_index = index

        # given (team 3 (cat C) plays teams 1 and 2 (cat A) in matchweeks 2,9,7,4)
        fixture_table = np.array([
            [0, 2, 7, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [2, 9, 0, 1, 8, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 3, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        fairness_constraint = FairnessConstraint(consecutive_hard_matches=2, penalty=1)

        # then
        self.assertFalse(fairness_constraint.is_violated(teams, fixture_table))

        # given (team 3 (index 2) plays against 1 (H) in matchweek 3, and against 2 (A) in matchweek 5
        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 4, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        self.assertTrue(fairness_constraint.is_violated(teams, fixture_table))

        # given (team 3 (index 2) plays against 1 (H) in matchweek 3, and against 2 (A) in matchweek 2
        fixture_table = np.array([
            [0, 2, 7, 4, 10, 6],
            [7, 0, 2, 10, 1, 8],
            [3, 9, 0, 1, 8, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 4, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        # then
        self.assertTrue(fairness_constraint.is_violated(teams, fixture_table))

        # given (team 4 category A)
        teams[3].category = 'A'
        # 3 (C) plays 1 in (2,7), plays 2 in (9,4) and plays 4 in (1, 6)
        fixture_table = np.array([
            [0, 2, 7, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [2, 9, 0, 1, 8, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 3, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        self.assertTrue(fairness_constraint.is_violated(teams, fixture_table))

        # given (consecutive games = 3)
        fairness_constraint.consecutive_hard_matches = 3
        self.assertFalse(fairness_constraint.is_violated(teams, fixture_table))

        # given (consecutive games = 3)
        # 3 (C) plays 1 in (2,7), plays 2 in (9,4) and plays 4 in (3, 6)
        fixture_table = np.array([
            [0, 2, 7, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [2, 9, 0, 3, 8, 5],
            [9, 5, 6, 0, 1, 2],
            [5, 6, 3, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        # then (consecutive matches 2,3,4)
        self.assertTrue(fairness_constraint.is_violated(teams, fixture_table))
