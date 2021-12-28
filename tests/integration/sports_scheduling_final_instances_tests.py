import json
from unittest import IsolatedAsyncioTestCase

from sports_scheduling.server import generate_schedule


class Test(IsolatedAsyncioTestCase):

    async def test_generate_schedule_5_teams(self):
        with open('problem_instances/final_instances/problem_teams_5_instance_1.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
        # print_from_response(result)

    async def test_generate_schedule_6_teams_72_penalties(self):
        with open('problem_instances/final_instances/problem_teams_6_penalties_72.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
        # print_from_response(result)

    async def test_generate_schedule_10_teams_92_penalties(self):
        with open('problem_instances/final_instances/problem_teams_10_penalties_92.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
        # print_from_response(result)

    async def test_generate_schedule_15_teams_151_penalties(self):
        with open('problem_instances/final_instances/problem_teams_15_penalties_151.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
        # print_from_response(result)

    async def test_generate_schedule_20_teams_159_penalties(self):
        with open('problem_instances/final_instances/problem_teams_20_penalties_159.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
        # print_from_response(result)
