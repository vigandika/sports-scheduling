from typing import List, Tuple

from numpy import ndarray

from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team
from sports_scheduling.util import get_team_by_id


class SharedVenueConstraint(BaseConstraint):

    def __init__(self, shared_venue_team_pairs: List[Tuple[int, int]]):
        """
        The pair of teams in shared venue constraint should have complementary H-A patterns

        :param shared_venue_team_pairs: a list containing pairs of id-s of the shared venue teams e.g. [(1,3), (2,4)] means that the pair of
                                        teams with ids 1 and 3 and the pair of teams with ids 2 and 4 are shared venue teams.
        """
        super().__init__(bracket='sharedVenueConstraint', level='HARD')

        assert isinstance(shared_venue_team_pairs, List)
        self.no_of_shared_venue_team_pairs = len(shared_venue_team_pairs)
        self.shared_venue_team_pairs = shared_venue_team_pairs

    def is_violated(self, teams: List[Team], fixture_table: ndarray):
        for team_pair in self.shared_venue_team_pairs:
            team_1 = get_team_by_id(teams, team_pair[0])
            team_2 = get_team_by_id(teams, team_pair[1])
            assert getattr(team_1, 'assigned_index') is not None and getattr(team_2, 'assigned_index') is not None, \
                f"either team with id {team_1.id} or team with id {team_2.id} have no assigned_index property"

            # If one of the matchweeks in team1's home games (row schedule) is in team2's home games, the constraint is violated
            for matchweek in fixture_table[team_1.assigned_index]:
                if matchweek in fixture_table[team_2.assigned_index] and matchweek != 0:
                    return True

            # If one of the matchweeks in team1's away games (column schedule) is in team2's away games?(maybe removed),
            # the constraint is violated
            for matchweek in fixture_table[:, team_1.assigned_index]:
                if matchweek in fixture_table[:, team_2.assigned_index] and matchweek != 0:
                    return True

            return False
