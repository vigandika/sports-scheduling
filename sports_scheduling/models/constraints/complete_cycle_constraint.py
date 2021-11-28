from sports_scheduling.models.constraints.base_constraint import BaseConstraint


class CompleteCycleConstraint(BaseConstraint):

    def __init__(self):
        """Each team should play once against each other team before playing a team for the second time"""
        super().__init__(bracket='completeCycleConstraint', level='HARD')

    def is_violated(self):
        pass
