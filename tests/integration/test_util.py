def print_from_response(response: dict):
    for matchweek, fixtures in response.items():
        matchweek_fixtures = f"""
            MATCHWEEK {matchweek.split('_')[-1]}:
        """
        for fixture in fixtures:
            matchweek_fixtures = f"{matchweek_fixtures}\n\t\t{fixture['homeTeam']} - {fixture['awayTeam']}"

        print(matchweek_fixtures)
