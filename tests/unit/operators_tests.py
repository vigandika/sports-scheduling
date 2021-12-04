from unittest import TestCase

import numpy as np

from sports_scheduling.models.teams.teams import Team
from sports_scheduling.operators import swap_homes, swap_schedules, swap_matchweeks


class OperatorsTests(TestCase):

    def test_swap_homes(self):
        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])
        t1 = Team(1, 'xyz', 'A')
        t2 = Team(2, 'xyz', 'A')
        t1.assigned_index = 0
        t2.assigned_index = 2

        mutated_fixture_table = swap_homes(fixture_table, t1, t2)
        np.testing.assert_array_equal(np.array([
            [0, 2, 3, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [8, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ]), mutated_fixture_table)

        t1.assigned_index = 4
        t2.assigned_index = 2
        mutated_fixture_table = swap_homes(fixture_table, t1, t2)
        np.testing.assert_array_equal(np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 2, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 7, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ]), mutated_fixture_table)

    def test_swap_schedules(self):
        t1 = Team(1, 'xyz', 'A')
        t2 = Team(2, 'xyz', 'A')
        t1.assigned_index = 0
        t2.assigned_index = 4

        swap_schedules(t1, t2)
        self.assertEqual(4, t1.assigned_index)
        self.assertEqual(0, t2.assigned_index)

    def test_swap_matchweeks(self):
        fixture_table = np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ])

        mutated_fixture_table = swap_matchweeks(fixture_table, 2, 8)
        np.testing.assert_array_equal(np.array([
            [0, 8, 2, 4, 10, 6],
            [7, 0, 4, 10, 1, 2],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 8],
            [5, 6, 8, 2, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ]), mutated_fixture_table)

        mutated_fixture_table = swap_matchweeks(fixture_table, 10, 3)
        np.testing.assert_array_equal(np.array([
            [0, 2, 8, 4, 3, 6],
            [7, 0, 4, 3, 1, 8],
            [10, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 10, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 10, 3, 7, 4, 0],
        ]), mutated_fixture_table)

        mutated_fixture_table = swap_matchweeks(fixture_table, 3, 3)
        np.testing.assert_array_equal(np.array([
            [0, 2, 8, 4, 10, 6],
            [7, 0, 4, 10, 1, 8],
            [3, 9, 0, 1, 7, 5],
            [9, 5, 6, 0, 3, 2],
            [5, 6, 2, 8, 0, 9],
            [1, 3, 10, 7, 4, 0],
        ]), mutated_fixture_table)

        self.assertRaises(AssertionError, swap_matchweeks, fixture_table, 3, 13)
        self.assertRaises(AssertionError, swap_matchweeks, fixture_table, 3, 0)
        self.assertRaises(AssertionError, swap_matchweeks, fixture_table, 3, 100)
        self.assertRaises(AssertionError, swap_matchweeks, fixture_table, -2, 2)
        self.assertRaises(AssertionError, swap_matchweeks, fixture_table, 0, 4)
