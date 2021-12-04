from unittest import TestCase
from unittest.mock import patch

import numpy as np

from sports_scheduling.models.constraints.encounter_constraint import EncounterConstraint
from sports_scheduling.models.teams.teams import Team


@patch('sports_scheduling.models.constraints.base_constraint.init_logging')
class EncounterConstraintTests(TestCase):

    @classmethod
    @patch('sports_scheduling.models.constraints.base_constraint.init_logging')
    def setUpClass(cls, _):
        cls.encounter_constraint = EncounterConstraint()

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

        self.assertFalse(self.encounter_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 0, 6],
            #            ^
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])

        self.assertTrue(self.encounter_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [0, 9, 0, 1, 7, 5],
            # ^
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])

        self.assertTrue(self.encounter_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 0, 7, 5],
            #         ^
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])

        self.assertTrue(self.encounter_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 0],
            #               ^
            [1, 3, 10, 7, 4, 0],
        ])

        self.assertTrue(self.encounter_constraint.is_violated(teams, fixture_table))
