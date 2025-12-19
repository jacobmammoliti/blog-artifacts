from models import Team

TEAMS: dict[int, Team] = {
    1: Team(id=1, nhl_id=24, name="Anaheim Ducks"),
    2: Team(id=2, nhl_id=6, name="Boston Bruins"),
    3: Team(id=3, nhl_id=7, name="Buffalo Sabres"),
    4: Team(id=6, nhl_id=20, name="Calgary Flames"),
    5: Team(id=4, nhl_id=12, name="Carolina Hurricanes"),
    6: Team(id=7, nhl_id=16, name="Chicago Blackhawks"),
    7: Team(id=8, nhl_id=21, name="Colorado Avalanche"),
    8: Team(id=5, nhl_id=29, name="Columbus Blue Jackets"),
    9: Team(id=9, nhl_id=25, name="Dallas Stars"),
    10: Team(id=10, nhl_id=17, name="Detroit Red Wings"),
    11: Team(id=11, nhl_id=22, name="Edmonton Oilers"),
    12: Team(id=12, nhl_id=13, name="Florida Panthers"),
    13: Team(id=13, nhl_id=26, name="Los Angeles Kings"),
    14: Team(id=14, nhl_id=30, name="Minnesota Wild"),
    15: Team(id=15, nhl_id=8, name="Montréal Canadiens"),
    16: Team(id=17, nhl_id=18, name="Nashville Predators"),
    17: Team(id=16, nhl_id=1, name="New Jersey Devils"),
    18: Team(id=18, nhl_id=2, name="New York Islanders"),
    19: Team(id=19, nhl_id=3, name="New York Rangers"),
    20: Team(id=20, nhl_id=9, name="Ottawa Senators"),
    21: Team(id=21, nhl_id=4, name="Philadelphia Flyers"),
    22: Team(id=22, nhl_id=5, name="Pittsburgh Penguins"),
    23: Team(id=24, nhl_id=28, name="San Jose Sharks"),
    24: Team(id=23, nhl_id=55, name="Seattle Kraken"),
    25: Team(id=25, nhl_id=19, name="St. Louis Blues"),
    26: Team(id=26, nhl_id=14, name="Tampa Bay Lightning"),
    27: Team(id=27, nhl_id=10, name="Toronto Maple Leafs"),
    28: Team(id=28, nhl_id=23, name="Vancouver Canucks"),
    29: Team(id=29, nhl_id=54, name="Vegas Golden Knights"),
    30: Team(id=30, nhl_id=15, name="Washington Capitals"),
    31: Team(id=31, nhl_id=52, name="Winnipeg Jets"),
    32: Team(id=32, nhl_id=68, name="Utah Mammoth"),
}

TEAMS_BY_NHL_ID: dict[int, Team] = {team.nhl_id: team for team in TEAMS.values()}

def get_team_by_nhl_id(nhl_id: int) -> Team | None:
    """Returns the team for a given NHL ID, or None if not found."""
    return TEAMS_BY_NHL_ID.get(nhl_id)