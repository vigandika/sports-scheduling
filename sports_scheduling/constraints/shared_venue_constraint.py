from typing import List, Tuple

from sports_scheduling.constraints.base_constraint import BaseConstraint


class SharedVenueConstraint(BaseConstraint):

    def __init__(self, shared_venue_team_pairs: List[Tuple[str, str]]):
        """The pair of teams in shared venue constraint should have complementary H-A patterns"""
        super().__init__(bracket='sharedVenueConstraint', level='HARD')
        self.no_of_shared_venue_teams = len(shared_venue_team_pairs)
        self.shared_venue_team_pairs = shared_venue_team_pairs

    def is_violated(self):
        pass
