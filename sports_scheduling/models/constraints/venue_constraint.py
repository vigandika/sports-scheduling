from sports_scheduling.models.constraints.base_constraint import BaseConstraint


class VenueConstraint(BaseConstraint):

    def __init__(self, team_id: int, venue: str, matchweek: int, penalty: int):
        """Forbid a team to play at a venue (H/A) in a certain matchweek"""
        super().__init__(bracket='venueConstraint', level='SOFT')
        self.team_id = team_id
        self.venue = venue
        self.matchweek = matchweek
        self.penalty = penalty

    def is_violated(self):
        pass
