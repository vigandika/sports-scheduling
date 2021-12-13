import json
from unittest import IsolatedAsyncioTestCase

from sports_scheduling.server import generate_schedule


class Test(IsolatedAsyncioTestCase):

    async def test_functionality(self):
        with open('problem_instances/problem_1_teams_6_instance.json') as data_file:
            data = json.load(data_file)
        result = await generate_schedule(data)
