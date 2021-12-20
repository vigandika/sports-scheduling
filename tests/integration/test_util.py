def print_from_response(response: dict):
    for index, matchweek in enumerate(response['matchweeks']):
        matchweek_fixtures = f"""
            MATCHWEEK {index + 1}:
        """
        for fixture in matchweek['fixtures']:
            matchweek_fixtures = f"{matchweek_fixtures}\n\t\t{fixture['homeTeam']} - {fixture['awayTeam']}"

        print(matchweek_fixtures)
