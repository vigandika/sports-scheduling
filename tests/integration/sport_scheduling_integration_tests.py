from unittest import TestCase
from unittest.mock import patch

from sports_scheduling.scheduler import Scheduler
from sports_scheduling.util import show_fixture_list


@patch('sports_scheduling.scheduler.init_logging')
class SportSchedulingTests(TestCase):

    def test_sports_scheduling_6(self, _):
        scheduler = Scheduler(number_of_teams=6, shared_venue_team_pairs=[(1, 3), (2, 4)])
        scheduler.generate()
        # print(scheduler.fixture_table)
        show_fixture_list(scheduler.fixture_table)

    def test_sports_scheduling_10(self, _):
        scheduler = Scheduler(10, [(1, 3), (2, 4)])
        scheduler.generate()
        # print(scheduler.fixture_table)
        show_fixture_list(scheduler.fixture_table)

    def test_sports_scheduling_20(self, _):
        scheduler = Scheduler(20, [(1, 3), (2, 4)])
        scheduler.generate()
        # print(scheduler.fixture_table)
        show_fixture_list(scheduler.fixture_table)
