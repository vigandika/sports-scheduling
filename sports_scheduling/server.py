from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sports_scheduling.log import get_logger
from sports_scheduling.models.constraints.shared_venue_constraint import SharedVenueConstraint
from sports_scheduling.scheduler import Scheduler
from sports_scheduling.simulated_annealing import SimulatedAnnealing
from sports_scheduling.util import assign_teams, parse_data, get_solution_response

app = FastAPI()

logging = get_logger(__name__)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# REMOVE THIS IN PROD

@app.post("/schedule")
async def generate_schedule(body: dict):
    try:
        teams, hard_constraints, soft_constraints = parse_data(body)

        # Get shared venue team pairs
        shared_venue_constraints = [constraint for constraint in hard_constraints if isinstance(constraint, SharedVenueConstraint)]

        # Extract the number of shared venue team pairs
        if len(shared_venue_constraints) > 1:
            raise RuntimeError('found more than 1 SharedVenueConstraint. Include all team pairs in teams of the one constraint')
        elif len(shared_venue_constraints) == 1:
            shared_venue_constraint = shared_venue_constraints[0]
        else:
            shared_venue_constraint = SharedVenueConstraint([])

        # generate initial solution
        scheduler = Scheduler(number_of_teams=len(teams), shared_venue_team_pairs=shared_venue_constraint.shared_venue_team_pairs)
        scheduler.generate()
        initial_solution = scheduler.fixture_table

        # assign indexes
        assign_teams(teams, shared_venue_constraint.shared_venue_team_pairs, scheduler.indexes_of_shared_venue_teams)

        # apply simulated annealing
        solution, teams = SimulatedAnnealing(hard_constraints, soft_constraints).run(initial_solution, teams)
        response = get_solution_response(solution, teams)

    except Exception as e:
        logging.exception(f'an error occurred')
        response = {"error": f"{e}"}

    return response
