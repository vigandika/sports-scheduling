from typing import List

from numpy import ndarray

from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team
from sports_scheduling.util import get_team_by_id


class VenueConstraint(BaseConstraint):

    def __init__(self, team_id: int, venue: str, matchweek: int, penalty: int):
        """Forbid a team to play at a venue (H/A) in a certain matchweek"""
        super().__init__(bracket='venueConstraint', level='SOFT')
        assert venue in ['H', 'A'], "venue should be one of 'H' (Home) or 'A' (Away)"

        self.team_id = team_id
        self.venue = venue
        self.matchweek = matchweek
        self.penalty = penalty

    def is_violated(self, teams: List[Team], fixture_table: ndarray) -> bool:
        team = get_team_by_id(teams, self.team_id)
        assert getattr(team, 'assigned_index') is not None, f"team with id {team.id} needs to have an 'assigned_index'"

        home_fixture_list, away_fixture_list = fixture_table[team.assigned_index], fixture_table[:, team.assigned_index]

        if self.venue == 'H':
            # Constraint is violated if the venue is 'H' and matchweek is in home fixture list
            return self.matchweek in home_fixture_list

        if self.venue == 'A':
            # Constraint is violated if the venue is 'A' and matchweek is in away fixture list
            return self.matchweek in away_fixture_list
