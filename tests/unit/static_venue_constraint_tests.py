from unittest import TestCase
from unittest.mock import patch

import numpy as np

from sports_scheduling.models.constraints.static_venue_constraint import StaticVenueConstraint
from sports_scheduling.models.teams.teams import Team


@patch('sports_scheduling.models.constraints.base_constraint.get_logger')
class StaticVenueConstraintTests(TestCase):
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
        static_venue_constraint = StaticVenueConstraint(maximum=2)
        self.assertFalse(static_venue_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 2, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        # then
        static_venue_constraint = StaticVenueConstraint(maximum=2)
        self.assertTrue(static_venue_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array(
            [[0, 4, 1, 6, 3, 10],
             [7, 0, 6, 8, 5, 1],
             [9, 2, 0, 5, 7, 8],
             [2, 3, 10, 0, 9, 4],
             [8, 10, 4, 1, 0, 6],
             [5, 9, 3, 7, 2, 0]]
        )
        # then
        static_venue_constraint = StaticVenueConstraint(maximum=2)
        self.assertTrue(static_venue_constraint.is_violated(teams, fixture_table))
