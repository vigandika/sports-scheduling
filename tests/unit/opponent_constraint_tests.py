from unittest import TestCase

import numpy as np

from sports_scheduling.models.constraints.opponent_constraint import OpponentConstraint
from sports_scheduling.models.teams.teams import Team


class OpponentConstraintTests(TestCase):

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
        opponent = OpponentConstraint(team_id=1, opponent_id=3, matchweek=8, penalty=1)
        self.assertTrue(opponent.is_violated(teams, fixture_table))

        opponent = OpponentConstraint(team_id=1, opponent_id=3, matchweek=3, penalty=1)
        self.assertTrue(opponent.is_violated(teams, fixture_table))

        opponent = OpponentConstraint(team_id=1, opponent_id=3, matchweek=1, penalty=1)
        self.assertFalse(opponent.is_violated(teams, fixture_table))

        opponent = OpponentConstraint(team_id=3, opponent_id=6, matchweek=5, penalty=1)
        self.assertTrue(opponent.is_violated(teams, fixture_table))

        opponent = OpponentConstraint(team_id=3, opponent_id=6, matchweek=10, penalty=1)
        self.assertTrue(opponent.is_violated(teams, fixture_table))

        opponent = OpponentConstraint(team_id=3, opponent_id=6, matchweek=8, penalty=1)
        self.assertFalse(opponent.is_violated(teams, fixture_table))
