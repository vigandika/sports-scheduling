from unittest import TestCase
from unittest.mock import patch

import numpy as np

from sports_scheduling.scheduler import Scheduler


@patch('sports_scheduling.scheduler.init_logging')
class SchedulerTests(TestCase):

    def test_check_hard_constraints_one_dimension(self, _):
        # given
        scheduler = Scheduler(6, 2)

        fixture_table = np.array([
            [1, 3, 4, 6, 0, 9],
            #            ^ target this
            [0, 0, 0, 0, 0, 13],
            [0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 0, 4],
        ])
        target_row, target_col = 0, 4
        # when (both values are not violations)
        value = scheduler.check_hard_constraints([8], target_row, target_col, fixture_table)
        self.assertEqual(8, value)

        value = scheduler.check_hard_constraints([8, 7], target_row, target_col, fixture_table)
        self.assertEqual(8, value)

        value = scheduler.check_hard_constraints([7, 8], target_row, target_col, fixture_table)
        self.assertEqual(7, value)

        repeater_violations = [1, 3, 4, 6, 9]
        consecutive_values_violations = [2, 5]
        # when (all but one tentative values are violations because are a repeater of another value in the row)
        value = scheduler.check_hard_constraints([7, *repeater_violations], target_row, target_col, fixture_table)
        self.assertEqual(7, value)

        value = scheduler.check_hard_constraints([*repeater_violations, 7], target_row, target_col, fixture_table)
        self.assertEqual(7, value)

        value = scheduler.check_hard_constraints([*repeater_violations, 7, *repeater_violations], target_row, target_col, fixture_table)
        self.assertEqual(7, value)

        # when (all but one tentative values are violations because cause the occurrence of 3 consecutive values)
        value = scheduler.check_hard_constraints([*consecutive_values_violations, 7], target_row, target_col, fixture_table)
        self.assertEqual(7, value)

        value = scheduler.check_hard_constraints([7, *consecutive_values_violations], target_row, target_col, fixture_table)
        self.assertEqual(7, value)

        value = scheduler.check_hard_constraints([*consecutive_values_violations, 7, *consecutive_values_violations], target_row,
                                                 target_col, fixture_table)
        self.assertEqual(7, value)

        # when (all but one tentative values are violations because cause the occurrence of either repetitive or 3 consecutive values)

        value = scheduler.check_hard_constraints([*consecutive_values_violations, 7, *repeater_violations], target_row, target_col,
                                                 fixture_table)
        self.assertEqual(7, value)

        value = scheduler.check_hard_constraints([*repeater_violations, 7, *consecutive_values_violations], target_row, target_col,
                                                 fixture_table)
        self.assertEqual(7, value)

        # when (all are violations)
        value = scheduler.check_hard_constraints([*consecutive_values_violations], target_row, target_col, fixture_table)
        self.assertIsNone(value)

        value = scheduler.check_hard_constraints([*repeater_violations], target_row, target_col, fixture_table)
        self.assertIsNone(value)

    def test_check_hard_constraints_two_dimensions(self, _):
        # given
        scheduler = Scheduler(6, 2)

        fixture_table = np.array([
            [1, 3, 4, 7, 9, 0],
            #               ^ target this
            [0, 0, 0, 0, 0, 13],
            [0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 0, 4],
        ])
        target_row, target_col = 0, 5

        # when (both values are not violations)
        value = scheduler.check_hard_constraints([10, 11, 12], target_row, target_col, fixture_table)
        self.assertEqual(10, value)

        value = scheduler.check_hard_constraints([11, 12, 10], target_row, target_col, fixture_table)
        self.assertEqual(11, value)

        row_violations = [1, 3, 4, 7, 9, 2, 5, 8]
        col_violations = [13, 2, 5, 4, 6, 3]

        # when (all but one are violations)
        value = scheduler.check_hard_constraints([11, *row_violations, *col_violations], target_row, target_col, fixture_table)
        self.assertEqual(11, value)

        value = scheduler.check_hard_constraints([*row_violations, *col_violations, 11], target_row, target_col, fixture_table)
        self.assertEqual(11, value)

        # when (all are row violations and one col violation)
        value = scheduler.check_hard_constraints([13, *row_violations], target_row, target_col, fixture_table)
        self.assertIsNone(value)

        # when (all row violations and one col violation)
        value = scheduler.check_hard_constraints([1, *col_violations], target_row, target_col, fixture_table)
        self.assertIsNone(value)

        # when (all are violations)
        value = scheduler.check_hard_constraints([*row_violations], target_row, target_col, fixture_table)
        self.assertIsNone(value)

        value = scheduler.check_hard_constraints([*col_violations], target_row, target_col, fixture_table)
        self.assertIsNone(value)

        value = scheduler.check_hard_constraints([*row_violations, *col_violations], target_row, target_col, fixture_table)
        self.assertIsNone(value)

    def test_check_hard_constraints_complementary_teams(self, _):
        # given
        scheduler = Scheduler(6, 2)

        fixture_table = np.array([
            [1, 2, 4, 7, 9, 0],
            #               ^ target this
            [0, 0, 0, 0, 0, 0],
            [4, 1, 5, 9, 8, 2],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        target_row, target_col = 0, 5
        complementary_team_index = 2

        self.assertEqual(5, scheduler.check_hard_constraints([5, 6], target_row, target_col, fixture_table))
        self.assertEqual(6, scheduler.check_hard_constraints([5, 6], target_row, target_col, fixture_table, complementary_team_index))

        # when (both values are not violations)
        value = scheduler.check_hard_constraints([6, 10], target_row, target_col, fixture_table, complementary_team_index)
        self.assertEqual(6, value)

        value = scheduler.check_hard_constraints([10, 6], target_row, target_col, fixture_table, complementary_team_index)
        self.assertEqual(10, value)

        # when (violating complementary team schedule)
        complementary_team_violations = fixture_table[complementary_team_index]

        value = scheduler.check_hard_constraints([10, *complementary_team_violations], target_row, target_col, fixture_table,
                                                 complementary_team_index)
        self.assertEqual(10, value)

        value = scheduler.check_hard_constraints([*complementary_team_violations, 11], target_row, target_col, fixture_table,
                                                 complementary_team_index)
        self.assertEqual(11, value)

        value = scheduler.check_hard_constraints([*complementary_team_violations], target_row, target_col, fixture_table,
                                                 complementary_team_index)
        self.assertIsNone(value)

    def test_check_n_consecutive_values(self, _):
        scheduler = Scheduler(6, 2)

        self.assertTrue(scheduler.find_n_consecutive_values(3, np.array([1, 3, 4, 8, 9, 12, 15]), 2))
        self.assertTrue(scheduler.find_n_consecutive_values(3, np.array([1, 3, 4, 8, 9, 12, 15]), 5))
        self.assertTrue(scheduler.find_n_consecutive_values(3, np.array([1, 3, 4, 8, 9, 12, 15]), 7))
        self.assertTrue(scheduler.find_n_consecutive_values(3, np.array([1, 2, 3, 5, 9, 12, 15]), 10))

        self.assertFalse(scheduler.find_n_consecutive_values(3, np.array([0, 1, 4, 8, 9, 12, 15]), 2))
        self.assertFalse(scheduler.find_n_consecutive_values(3, np.array([1, 3, 4, 8, 9, 12, 15]), 8))
        self.assertFalse(scheduler.find_n_consecutive_values(3, np.array([1, 3, 4, 8, 9, 12, 15]), 11))

        self.assertTrue(scheduler.find_n_consecutive_values(3, np.array([1, 3, 5, 7, 9, 12]), 2))
        self.assertTrue(scheduler.find_n_consecutive_values(3, np.array([1, 3, 5, 7, 9, 12]), 4))
        self.assertTrue(scheduler.find_n_consecutive_values(3, np.array([1, 3, 5, 7, 9, 12]), 6))
        self.assertTrue(scheduler.find_n_consecutive_values(3, np.array([1, 3, 5, 7, 9, 12]), 8))

        self.assertFalse(scheduler.find_n_consecutive_values(3, np.array([1, 3, 5, 7, 9, 12]), 10))
        self.assertFalse(scheduler.find_n_consecutive_values(3, np.array([1, 3, 5, 7, 9, 12]), 1))

        self.assertTrue(scheduler.find_n_consecutive_values(4, np.array([1, 2, 4, 8, 9, 12, 15]), 3))
        self.assertFalse(scheduler.find_n_consecutive_values(4, np.array([1, 2, 4, 8, 9, 12, 15]), 10))

        self.assertTrue(scheduler.find_n_consecutive_values(5, np.array([1, 2, 4, 5, 9, 12, 15]), 3))
