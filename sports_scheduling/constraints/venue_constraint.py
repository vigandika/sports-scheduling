from sports_scheduling.constraints.base_constraint import BaseConstraint


class VenueConstraint(BaseConstraint):

    def __init__(self):
        """Forbid a team to play at a venue (H/A) in a certain matchweek"""
        super().__init__(bracket='venueConstraint', level='SOFT')

    def is_violated(self):
        pass
