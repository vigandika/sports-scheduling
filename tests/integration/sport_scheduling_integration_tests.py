from unittest import TestCase
from unittest.mock import patch

from sports_scheduling.scheduler import Scheduler
from sports_scheduling.util import show_fixture_list


@patch('sports_scheduling.scheduler.init_logging')
class SportSchedulingTests(TestCase):

    def test_sports_scheduling_6(self, _):
        scheduler = Scheduler(6, 2)
        scheduler.solve()
        print(scheduler.fixture_table)
        # show_fixture_list(scheduler.fixture_table)

    def test_sports_scheduling_10(self, _):
        scheduler = Scheduler(10, 2)
        scheduler.solve()
        print(scheduler.fixture_table)
        show_fixture_list(scheduler.fixture_table)

    def test_sports_scheduling_20(self, _):
        scheduler = Scheduler(20, 3)
        scheduler.solve()
        print(scheduler.fixture_table)
        show_fixture_list(scheduler.fixture_table)
