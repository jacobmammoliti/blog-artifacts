import requests
from pydantic import BaseModel

class Team(BaseModel):
    id: int
    nhl_id: int
    name: str

    def get_team_last_10_games(self, wtp_api_base: str) -> dict:
        request = requests.get(f"{wtp_api_base}/{self.id}/games")

        return request.json()

class Game(BaseModel):
    homeTeam: Team
    homeTeamGames: list[dict]
    awayTeam: Team
    awayTeamGames: list[dict]