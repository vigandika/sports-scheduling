from typing import List

from numpy import ndarray

from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.teams.teams import Team


class EncounterConstraint(BaseConstraint):

    def __init__(self):
        """Every team should play against every other team, once H and once A"""
        super().__init__(bracket='encounterConstraint', level='HARD')

    def is_violated(self, teams: List[Team], fixture_table: ndarray):
        for team in teams:
            assert getattr(team, 'assigned_index') is not None, f"team {team.name} needs to have an 'assigned_index'"

            # team 0 (row=0) plays against team 2 (col=2) at the intersection (0,2) in matchweek fixture_table[0, 2]
            # Check that no zero matchweeks exist in home matches fixture list (fixture_table[row]) for team
            for opponent_index, matchweek in enumerate(fixture_table[team.assigned_index]):
                if opponent_index != team.assigned_index and matchweek == 0:
                    # If the intersection with a team other than itself (opponent_index!=assigned_index) is zero it means the team does not
                    # have a specified matchweek to play against team opponent_index, thus the constraint is violated
                    return True

            # Check that no zero matchweeks exist in home matches fixture list (fixture_table[row]) for team
            for opponent_index, matchweek in enumerate(fixture_table[:, team.assigned_index]):
                if opponent_index != team.assigned_index and matchweek == 0:
                    # If the intersection with a team other than itself (opponent_index!=assigned_index) is zero it means the team does not
                    # have a specified matchweek to play against team opponent_index, thus the constraint is violated
                    return True

        return False
