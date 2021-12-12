from unittest import TestCase
from unittest.mock import patch

import numpy as np

from sports_scheduling.models.constraints.repeater_gap_constraint import RepeaterGapConstraint
from sports_scheduling.models.teams.teams import Team


@patch('sports_scheduling.models.constraints.base_constraint.get_logger')
class RepeaterGapConstraintTests(TestCase):
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
        # then
        repeater_gap_constraint = RepeaterGapConstraint(team1_id=1, team2_id=4, minimum_gap=5, penalty=1)
        self.assertFalse(repeater_gap_constraint.is_violated(teams, fixture_table))

        repeater_gap_constraint = RepeaterGapConstraint(team1_id=1, team2_id=4, minimum_gap=1, penalty=1)
        self.assertFalse(repeater_gap_constraint.is_violated(teams, fixture_table))

        repeater_gap_constraint = RepeaterGapConstraint(team1_id=1, team2_id=4, minimum_gap=10, penalty=1)
        self.assertTrue(repeater_gap_constraint.is_violated(teams, fixture_table))

        repeater_gap_constraint = RepeaterGapConstraint(team1_id=1, team2_id=4, minimum_gap=6, penalty=1)
        self.assertTrue(repeater_gap_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [8, 5, 6, 0, 3, 2],
            # ^ 9 turned to 8
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        # then
        repeater_gap_constraint = RepeaterGapConstraint(team1_id=1, team2_id=4, minimum_gap=5, penalty=1)
        self.assertTrue(repeater_gap_constraint.is_violated(teams, fixture_table))

        repeater_gap_constraint = RepeaterGapConstraint(team1_id=1, team2_id=4, minimum_gap=4, penalty=1)
        self.assertFalse(repeater_gap_constraint.is_violated(teams, fixture_table))

        repeater_gap_constraint = RepeaterGapConstraint(team1_id=1, team2_id=4, minimum_gap=6, penalty=1)
        self.assertTrue(repeater_gap_constraint.is_violated(teams, fixture_table))
