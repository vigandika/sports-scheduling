import json
from unittest import IsolatedAsyncioTestCase

from sports_scheduling.server import generate_schedule
from tests.integration.test_util import print_from_response


class Test(IsolatedAsyncioTestCase):

    async def test_generate_schedule_6_teams(self):
        with open('problem_instances/problem_1_teams_6_instance.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
        print_from_response(result)

    async def test_generate_schedule_6_teams_problem_2(self):
        with open('problem_instances/problem_2_teams_6_instance.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
        print_from_response(result)

    async def test_generate_schedule_10_teams(self):
        with open('problem_instances/problem_3_teams_10_instance.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
        print_from_response(result)
