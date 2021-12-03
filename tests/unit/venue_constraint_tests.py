from unittest import TestCase

import numpy as np

from sports_scheduling.models.constraints.venue_constraint import VenueConstraint
from sports_scheduling.models.teams.teams import Team


class VenueConstraintTests(TestCase):

    def test_is_violated(self):
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

        # team with id 1 (assigned_index=0) plays with team with id 3 (assigned_index=2) in matchweek 8
        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        # then
        venue_constraint = VenueConstraint(team_id=1, venue='A', matchweek=8, penalty=1)
        self.assertFalse(venue_constraint.is_violated(teams, fixture_table))

        venue_constraint = VenueConstraint(team_id=2, venue='H', matchweek=5, penalty=1)
        self.assertFalse(venue_constraint.is_violated(teams, fixture_table))

        venue_constraint = VenueConstraint(team_id=3, venue='A', matchweek=1, penalty=1)
        self.assertFalse(venue_constraint.is_violated(teams, fixture_table))

        venue_constraint = VenueConstraint(team_id=3, venue='A', matchweek=3, penalty=1)
        self.assertFalse(venue_constraint.is_violated(teams, fixture_table))

        venue_constraint = VenueConstraint(team_id=4, venue='A', matchweek=3, penalty=1)
        self.assertFalse(venue_constraint.is_violated(teams, fixture_table))

        venue_constraint = VenueConstraint(team_id=4, venue='H', matchweek=3, penalty=1)
        self.assertTrue(venue_constraint.is_violated(teams, fixture_table))

        venue_constraint = VenueConstraint(team_id=1, venue='A', matchweek=1, penalty=1)
        self.assertTrue(venue_constraint.is_violated(teams, fixture_table))

        venue_constraint = VenueConstraint(team_id=6, venue='H', matchweek=7, penalty=1)
        self.assertTrue(venue_constraint.is_violated(teams, fixture_table))
