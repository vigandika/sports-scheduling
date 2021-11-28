from sports_scheduling.constraints.base_constraint import BaseConstraint


class SharedVenueConstraint(BaseConstraint):

    def __init__(self):
        """The pair of teams in shared venue constraint should have complementary H-A patterns"""
        super().__init__(bracket='sharedVenueConstraint', level='HARD')

    def is_violated(self):
        pass
