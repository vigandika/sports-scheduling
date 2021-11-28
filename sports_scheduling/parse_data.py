import json
from typing import List

from sports_scheduling.models.constraints.base_constraint import BaseConstraint
from sports_scheduling.models.constraints.complete_cycle_constraint import CompleteCycleConstraint
from sports_scheduling.models.constraints.encounter_constraint import EncounterConstraint
from sports_scheduling.models.constraints.fairness_constraint import FairnessConstraint
from sports_scheduling.models.constraints.opponent_constraint import OpponentConstraint
from sports_scheduling.models.constraints.participation_constraint import ParticipationConstraint
from sports_scheduling.models.constraints.repeater_gap_constraint import RepeaterGapConstraint
from sports_scheduling.models.constraints.shared_venue_constraint import SharedVenueConstraint
from sports_scheduling.models.constraints.static_venue_constraint import StaticVenueConstraint
from sports_scheduling.models.constraints.venue_constraint import VenueConstraint
from sports_scheduling.models.teams.teams import Team

teams: List[Team] = []
soft_constraints: List[BaseConstraint] = []
hard_constraints: List[BaseConstraint] = []
with open('models/test_json_outlook.json') as f:
    data = json.load(f)
    try:
        for team in data["teams"]:
            teams.append(Team(id=team['id'], name=team['name'], category=team['category']))
    except Exception:
        raise RuntimeError(f"an expected error occurred when processing team {team} in data {data}")

    try:
        for constraint in data['constraints']:
            if constraint['level'] == 'HARD':
                if constraint['type'] == 'completeCycleConstraint':
                    hard_constraints.append(CompleteCycleConstraint())
                elif constraint['type'] == 'encounterConstraint':
                    hard_constraints.append(EncounterConstraint())
                elif constraint['type'] == 'participationConstraint':
                    hard_constraints.append(ParticipationConstraint())
                elif constraint['type'] == 'staticVenueConstraint':
                    hard_constraints.append(StaticVenueConstraint(maximum=constraint['maximum']))
                elif constraint['type'] == 'sharedVenueConstraint':
                    hard_constraints.append(SharedVenueConstraint(shared_venue_team_pairs=constraint['teams']))
                else:
                    raise TypeError(f"unrecognized hard constraint type '{constraint['type']}'")

            elif constraint['level'] == 'SOFT':
                if constraint['type'] == 'opponentConstraint':
                    soft_constraints.append(OpponentConstraint(team_id=constraint['teamId'], opponent_id=constraint['opponentId'],
                                                               matchweek=constraint['matchweek'], penalty=constraint['penalty']))
                elif constraint['type'] == 'venueConstraint':
                    soft_constraints.append(VenueConstraint(team_id=constraint['teamId'], venue=constraint['venue'],
                                                            matchweek=constraint['venue'], penalty=constraint['penalty']))
                elif constraint['type'] == 'repeaterGapConstraint':
                    soft_constraints.append(RepeaterGapConstraint(team1_id=constraint['team1Id'], team2_id=constraint['team2Id'],
                                                                  minimum_gap=constraint['minimumGap'], penalty=constraint['penalty']))
                elif constraint['type'] == 'fairnessConstraint':
                    soft_constraints.append(FairnessConstraint(consecutive_hard_matches=constraint['consecutiveHardMatches']))
                else:
                    raise TypeError(f"unrecognized soft constraint type '{constraint['type']}'")
            else:
                raise TypeError(f"unrecognized level type '{constraint['type']}'")
    except Exception:
        raise RuntimeError(f"an expected error occurred when processing constraint {constraint} in data {data}")
