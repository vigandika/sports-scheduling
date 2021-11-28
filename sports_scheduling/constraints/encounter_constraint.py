from sports_scheduling.constraints.base_constraint import BaseConstraint


class EncounterConstraint(BaseConstraint):

    def __init__(self):
        """Every team should play against every other team, once H and once A"""
        super().__init__(bracket='encounterConstraint', level='HARD')

    def is_violated(self):
        pass
