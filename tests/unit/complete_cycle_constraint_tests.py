from unittest import TestCase
from unittest.mock import patch

import numpy as np

from sports_scheduling.models.constraints.complete_cycle_constraint import CompleteCycleConstraint
from sports_scheduling.models.teams.teams import Team


@patch('sports_scheduling.models.constraints.base_constraint.get_logger')
class CompleteCycleConstraintTests(TestCase):

    @classmethod
    @patch('sports_scheduling.models.constraints.base_constraint.get_logger')
    def setUpClass(cls, _):
        cls.complete_cycle_constraint = CompleteCycleConstraint()

    def test_is_violated(self, _):
        teams = [
            Team(1, 'xyz', 'A'),
            Team(2, 'xyz', 'A'),
            Team(3, 'xyz', 'A'),
            Team(4, 'xyz', 'A'),
            Team(5, 'xyz', 'A'),
            Team(6, 'xyz', 'A'),
        ]

        for index in range(len(teams)):
            teams[index].assigned_index = index

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        self.assertFalse(self.complete_cycle_constraint.is_violated(teams, fixture_table))

        # Team 0 plays against team 2 in matchweek 3 & 4. Consequently, it plays against team 3 in matchweek 8 and 9
        fixture_table = np.array([
            [0, 2, 4, 8, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        self.assertTrue(self.complete_cycle_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 3, 6],
            #            ^ Changed to 3
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        self.assertTrue(self.complete_cycle_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 10, 3, 4, 7, 0],
            # Team 5 plays Team 2 in matchweek 3 & 5. Also T5 plays T4 in matchweeks 7 & 9.
        ])
        self.assertTrue(self.complete_cycle_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 5, 7, 1],
            # Team 2 plays against T3 in matchweeks 5 & 6.
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        self.assertFalse(self.complete_cycle_constraint.is_violated(teams, fixture_table))
