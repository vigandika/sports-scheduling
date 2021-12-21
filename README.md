# sports-scheduling ⚽⏱

## Problem ☔

Create a scheduling solution for sports competitions that will satisfy all of given HARD constraints and minimally violate given
soft constraints.

### Constraints

* `ParticipationConstraint (HARD)`- Every team should play exactly once at each matchweek
* `CompleteCycleConstraint (HARD)` - Each team should play once against each other team before playing a team for the second time
* `EncounterConstraint (HARD)` - Every team should play against every other team, once Home and once Away
* `StaticVenueConstraint (HARD)` - Limit the number of consecutive games a team can play in the same venue
* `SharedVenueConstraint (HARD)` - Synchronize the schedule of a pair of teams that share a venue to have complementary H-A patterns
* `FairnessConstraint (SOFT)` - Limit the number of consecutive games a low level team can play against the strongest teams
* `OpponentConstraint (SOFT)` - Forbid a team to play against an opponent in a given matchweek
* `VenueConstraint (SOFT)` - Forbid a team to play at a venue (H/A) in a certain matchweek
* `RepeaterGapConstraint (SOFT)` - Regulate the minimum number of rounds to be played before two teams meet for the second time

## Requirements
* Python 3 (tested with 3.8)
* [Conda](https://conda.io/)

## Environment

[Conda](https://conda.io/) is used as the package, dependency and environment manager. The dependencies of the application are defined in
the file `environment.yml`

The Conda environment can be set up using `environment.yml`:

```bash
conda env create -f environment.yml
```

After creating the environment, configure the Python Interpreter to use the new environment. In PyCharm (as of v2021.2.3), go to
`Settings` > `Python Interpreter` and Click the setting gear icon besides the Python Interpreter drop down list.
The `Add Python Interpreter` window should pop up.  
Navigate to `Conda Enviornment` in the left-hand side > Check `Existing environment` and choose the executable interpreter from the
environment path you just created.

## Run it 🚦

After setting up the environment one will have [uvicorn](https://www.uvicorn.org/) installed and can start up the server by running:

```bash
uvicorn sports_scheduling.server:app --port 9090
```
*Make sure you are in the project root directory: `sports-scheduling$ `

After running the command the server should be up and running and listening for requests in [localhost:9090](http://localhost:9090).

The server understands only one request and that is a `POST` request to the `/schedule` endpoint.

### Request Body

The response body should be a valid JSON containing the teams the application should generate the schedule for and the constraints to obey. 
The JSON should have the following structure:

```json
{
    "teams": [
      {"id": 1, "name": "Prishtina", "category": "A"},
      {"id": 2, "name": "Flamurtari", "category": "B"}
    ],
    "constraints": [
      {"type": "completeCycleConstraint", "level": "HARD"},
      {"type": "encounterConstraint", "level": "HARD"},
      {"type": "participationConstraint", "level": "HARD"},
      {"type": "staticVenueConstraint", "level": "HARD", "maximum": 3},
      {"type": "sharedVenueConstraint", "level": "HARD", "teams": [[1, 2], [3, 4]]},
      {"type": "opponentConstraint", "level": "SOFT", "penalty": 1, "teamId": 4, "opponentId": 6, "matchweek": 5},
      {"type": "venueConstraint", "level": "SOFT", "penalty": 2, "teamId": 9, "venue": "A", "matchweek": 3},
      {"type": "repeaterGapConstraint", "level": "SOFT", "penalty": 3, "team1Id": 3, "team2Id": 8, "minimumGap": 8}
    ]
}
```

The minimum number of different teams to compete is 5. The maximum is unlimited. If the number of teams competing is odd, each team
will get a [bye](https://en.wikipedia.org/wiki/Bye_(sports)) twice, indicating a round in which that particular team will not participate.

There should be exactly one of each hard constraints and an unlimited number of soft constraints. Each type of soft constraints should
have the properties listed above. The `penalty` in soft constraints is an integer from 1-5 that describes the importance of a constraint to
be satisfied, with 5 being most important. The algorithm will give advantage and try to satisfy the constraints with the highest `penalty`.

For examples, check problem instances under `/tests/integration/problem_instances/`.

### Run it using integration tests

Alternatively, one can run the application without starting the server by running the integration tests under 
`/tests/integration/sports_scheduling_integration.tests.py`. The data should be read from one of the files (or create a new one) in the
`/tests/problem_instances/`. 

## Trivia

The word 'matchweek' will probably appear as a typo in your IDE because it's not an official word in the English Language. However, because
this terminology is heavily used in football competitions, I decided to use it in the project as well. If the underline annoys you
(like it did to me), you can add it in the dictionary of your IDE, so it doesn't show it as a typo anymore. 
The way to do this in PyCharm (v2021.2.3) is by hovering over the green underlined word, clicking "More Actions" > "Save to dictionary".
