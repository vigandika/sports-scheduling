"""

teams = parse_data()
soft_constraints = parse_data()
hard_constraints = parse_date()

initial_solution = scheduler.generate(number_of_teams, number_of_shared_venue_pairs)

assign_indexes()
    - assign indexes of the teams. Link team.id with team.assigned_index. A place to sort out shared venue teams

simulated_annealing(initial_solution, teams, soft_constraints, hard_constraints)
    scheduler_fitness(teams, soft_constraints, hard_constraints)

"""

from parse_data import teams, soft_constraints, hard_constraints  # These will be taken from the request
from sports_scheduling.models.constraints.shared_venue_constraint import SharedVenueConstraint
from sports_scheduling.scheduler import Scheduler
from sports_scheduling.simulated_annealing import SimulatedAnnealing

shared_venue_constraints = [soft_constraint for soft_constraint in soft_constraints if isinstance(soft_constraint, SharedVenueConstraint)]

# Extract the number of shared venue team pairs
if len(shared_venue_constraints) > 1:
    raise RuntimeError('found more than 1 SharedVenueConstraint. Include all team pairs in teams of the one constraint')
elif len(shared_venue_constraints) == 1:
    shared_venue_constraint = shared_venue_constraints[0]
else:
    shared_venue_constraint = 0

initial_solution = Scheduler(number_of_teams=len(teams), number_of_shared_venue_pairs=shared_venue_constraint.no_of_shared_venue_team_pairs)

# assign indexes

SimulatedAnnealing.solve(initial_solution.fixture_table, teams, hard_constraints, soft_constraints)
