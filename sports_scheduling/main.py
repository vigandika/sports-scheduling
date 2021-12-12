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

from parse_data import teams, hard_constraints, soft_constraints  # These will be taken from the request
from sports_scheduling.models.constraints.shared_venue_constraint import SharedVenueConstraint
from sports_scheduling.scheduler import Scheduler
from sports_scheduling.simulated_annealing import SimulatedAnnealing
from sports_scheduling.util import assign_teams, print_fixture_list

shared_venue_constraints = [hard_constraint for hard_constraint in hard_constraints if isinstance(hard_constraint, SharedVenueConstraint)]

# Extract the number of shared venue team pairs
if len(shared_venue_constraints) > 1:
    raise RuntimeError('found more than 1 SharedVenueConstraint. Include all team pairs in teams of the one constraint')
elif len(shared_venue_constraints) == 1:
    shared_venue_constraint = shared_venue_constraints[0]
else:
    shared_venue_constraint = []

# Create initial solution
scheduler = Scheduler(number_of_teams=len(teams), shared_venue_team_pairs=shared_venue_constraint.shared_venue_team_pairs)
scheduler.generate()
initial_solution = scheduler.fixture_table
# assign indexes
assign_teams(teams, shared_venue_constraint.shared_venue_team_pairs)
# Show fixture list
# print_fixture_list(initial_solution, teams)

solution, teams = SimulatedAnnealing(hard_constraints, soft_constraints).run(initial_solution, teams)
print_fixture_list(solution, teams)
