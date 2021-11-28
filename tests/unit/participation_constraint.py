from unittest import TestCase

import numpy as np

from sports_scheduling.models.constraints.participation_constraint import ParticipationConstraint
from sports_scheduling.models.teams.teams import Team


class ParticipationConstraintTests(TestCase):
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

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        # then
        participation_constraint = ParticipationConstraint()
        self.assertFalse(participation_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 0, 6],
            #             ^ 10 missing
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        # then
        participation_constraint = ParticipationConstraint()
        self.assertTrue(participation_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [0, 5, 6, 0, 3, 2],
            # ^9 missing
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        # then
        participation_constraint = ParticipationConstraint()
        self.assertTrue(participation_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 11, 8, 0, 9],
            #       ^ 2 is 11
            [1, 3, 10, 7, 4, 0],
        ])
        # then
        participation_constraint = ParticipationConstraint()
        self.assertTrue(participation_constraint.is_violated(teams, fixture_table))

        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 10, 7, 5],
            #          ^1 is 10
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        # them
        participation_constraint = ParticipationConstraint()
        self.assertTrue(participation_constraint.is_violated(teams, fixture_table))
