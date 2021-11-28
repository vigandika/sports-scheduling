from sports_scheduling.constraints.base_constraint import BaseConstraint


class VenueConstraint(BaseConstraint):

    def __init__(self, team, venue, matchweek: int, penalty: int):
        """Forbid a team to play at a venue (H/A) in a certain matchweek"""
        super().__init__(bracket='venueConstraint', level='SOFT')
        self.team = team
        self.venue = venue
        self.matchweek = matchweek
        self.penalty = penalty

    def is_violated(self):
        pass
