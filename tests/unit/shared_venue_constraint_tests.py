from unittest import TestCase
from unittest.mock import patch

import numpy as np

from sports_scheduling.models.constraints.shared_venue_constraint import SharedVenueConstraint
from sports_scheduling.models.teams.teams import Team


@patch('sports_scheduling.models.constraints.base_constraint.get_logger')
class SharedVenueConstraintTests(TestCase):

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
        shared_venue_constraint = SharedVenueConstraint(shared_venue_team_pairs=[(1, 3), (2, 4)])
        self.assertFalse(shared_venue_constraint.is_violated(teams, fixture_table))

        shared_venue_constraint = SharedVenueConstraint(shared_venue_team_pairs=[(3, 1), (4, 2)])
        self.assertFalse(shared_venue_constraint.is_violated(teams, fixture_table))

        shared_venue_constraint = SharedVenueConstraint(shared_venue_team_pairs=[(1, 4)])
        self.assertTrue(shared_venue_constraint.is_violated(teams, fixture_table))

        shared_venue_constraint = SharedVenueConstraint(shared_venue_team_pairs=[(2, 3)])
        self.assertTrue(shared_venue_constraint.is_violated(teams, fixture_table))

        shared_venue_constraint = SharedVenueConstraint(shared_venue_team_pairs=[(1, 5)])
        self.assertTrue(shared_venue_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 6, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        shared_venue_constraint = SharedVenueConstraint(shared_venue_team_pairs=[(1, 3), (2, 4)])
        self.assertTrue(shared_venue_constraint.is_violated(teams, fixture_table))

    def test_is_violated_second_pair(self, _):
        f = np.array([[0, 4, 8, 1, 5, 10],
                      [7, 0, 1, 5, 2, 8],
                      [3, 9, 0, 2, 7, 6],
                      [9, 6, 10, 0, 3, 4],
                      [6, 10, 4, 8, 0, 1],
                      [2, 3, 5, 7, 9, 0]])
        teams = [
            Team(1, 'xyz-1', 'A'),
            Team(2, 'xyz-2', 'A'),
            Team(3, 'xyz-3', 'A'),
            Team(4, 'xyz-4', 'A'),
            Team(5, 'xyz-5', 'A'),
            Team(6, 'xyz-6', 'A'),
        ]

        teams[0].assigned_index = 0
        teams[1].assigned_index = 2
        teams[2].assigned_index = 1
        teams[3].assigned_index = 3
        teams[4].assigned_index = 4
        teams[5].assigned_index = 5

        # then
        shared_venue_constraint = SharedVenueConstraint(shared_venue_team_pairs=[(1, 2), (3, 4)])
        self.assertFalse(shared_venue_constraint.is_violated(teams, f))
