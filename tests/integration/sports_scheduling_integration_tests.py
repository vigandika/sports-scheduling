import json
from unittest import IsolatedAsyncioTestCase

from sports_scheduling.server import generate_schedule
from tests.integration.test_util import print_from_response


class Test(IsolatedAsyncioTestCase):

    async def test_generate_schedule_6_teams(self):
        with open('problem_instances/problem_teams_6_instance_1.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
        print_from_response(result)

    async def test_generate_schedule_6_teams_instance_2(self):
        with open('problem_instances/problem_teams_6_instance_2.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
        print_from_response(result)

    async def test_generate_schedule_10_teams(self):
        with open('problem_instances/problem_teams_10_instance_1.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
        print_from_response(result)

    async def test_generate_schedule_5_teams(self):
        with open('problem_instances/problem_teams_5_instance_1.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
        print_from_response(result)