from sports_scheduling.constraints.base_constraint import BaseConstraint


class FairnessConstraint(BaseConstraint):

    def __init__(self, consecutive_hard_matches: int):
        """No C-class team should play more than 3 consecutive matches against A-class team"""
        super().__init__(bracket='fairnessConstraint', level='SOFT')
        self.consecutive_hard_matches = consecutive_hard_matches

    def is_violated(self):
        pass
