# sports-scheduling

## Problem

Create a scheduling solution for sports competitions that will satisfy all of various custom HARD constraints and minimally violate given
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

## Run it

After adjusting the environment, you can run a demo problem for different test cases in the integration tests file located in 
`tests/integration/sports_scheduling_integration_tests.py`, giving the two parameters as you please: `number_of_teams` and 
`number_of_shared_venue_pairs`.

## Trivia

The word 'matchweek' will probably appear as a typo in your IDE because it's not an official word in the English Language. However, because
this terminology is heavily used in football competitions, I decided to use it in the project as well. If the underline annoys you
(like it did to me), you can add it in the dictionary of your IDE, so it doesn't show it as a typo anymore. 
The way to do this in PyCharm (v2021.2.3) is by hovering over the green underlined word, clicking "More Actions" >  "Save to dictionary".