from unittest import TestCase

from sports_scheduling.scheduler import Scheduler
from sports_scheduling.util import show_fixture_list


class SportSchedulingTests(TestCase):

    def test_sports_scheduling_6(self):
        scheduler = Scheduler(number_of_teams=6, shared_venue_team_pairs=[(1, 3), (2, 4)])
        scheduler.generate()
        print(scheduler.fixture_table)
        show_fixture_list(scheduler.fixture_table)

    def test_sports_scheduling_10(self):
        scheduler = Scheduler(10, [(1, 3), (2, 4)])
        scheduler.generate()
        # print(scheduler.fixture_table)
        show_fixture_list(scheduler.fixture_table)

    def test_sports_scheduling_20(self):
        scheduler = Scheduler(20, [(1, 3), (2, 4)])
        scheduler.generate()
        # print(scheduler.fixture_table)
        show_fixture_list(scheduler.fixture_table)
