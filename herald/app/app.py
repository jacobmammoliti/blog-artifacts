from teams import get_team_by_nhl_id
from models import Game
from settings import ANALYSIS_PROMPT

import logging

import requests
from requests.exceptions import HTTPError

from datetime import date
from google import genai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from pydantic_settings import BaseSettings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class Config(BaseSettings):
    slack_bot_token: str
    channel_id: str
    llm_model: str = "gemini-3-pro-preview"
    nhl_api_base: str = "https://api-web.nhle.com/v1/score"
    wtp_api_base: str = "http://127.0.0.1:8000/api/v1/teams"

    @property
    def slack_client(self):
        return WebClient(token=self.slack_bot_token)

def get_tonight_schedule() -> dict:
    today = date.today().strftime("%Y-%m-%d")
    logger.info(f"Fetching tonight's schedule from {config.nhl_api_base}/{today}")

    try:
        response = requests.get(f"{config.nhl_api_base}/{today}")
        response.raise_for_status()
    except HTTPError:
        raise

    schedule = response.json()['games']

    return schedule

def parse_schedule(schedule: dict) -> list[Game]:
    games = []

    for game in schedule:
        home_team = get_team_by_nhl_id(game['homeTeam']['id'])
        away_team = get_team_by_nhl_id(game['awayTeam']['id'])
        
        if home_team is None or away_team is None:
            raise TypeError(
                f"""
                Unable to process home and away team.
                Got {home_team} for home team.
                Got {away_team} for away team.
                """)

        game_details = Game(
            homeTeam=home_team,
            homeTeamGames=home_team.get_team_last_10_games(config.wtp_api_base), # pyright: ignore[reportArgumentType]
            awayTeam=away_team,
            awayTeamGames=away_team.get_team_last_10_games(config.wtp_api_base) # pyright: ignore[reportArgumentType]
        )
        
        games.append(game_details)
        
        logger.info(f"Parsed game for {away_team.name} @ {home_team.name}")
    
    return games

def analyze_game(game: Game) -> str:
    genai_client = genai.Client()

    prompt = ANALYSIS_PROMPT.format(
        game_date=date.today().strftime("%Y-%m-%d"),
        away_team=game.awayTeam.name,
        away_team_games=game.awayTeamGames,
        home_team=game.homeTeam.name,
        home_team_games=game.homeTeamGames
    )

    response = genai_client.models.generate_content(
        model=config.llm_model,
        contents=prompt
    )

    if not response.text:
        raise ValueError(
            f"""
            Unable to generate analysis for game:
            {game.awayTeam.name} @ {game.homeTeam.name}
            """)

    return response.text

def post_to_slack(message: str, thread_ts: str = None) -> dict:
    try:
        response = config.slack_client.chat_postMessage(
            channel=config.channel_id,
            markdown_text=message,
            thread_ts=thread_ts
        )
        return response
    except SlackApiError:
        raise

def analyze_and_post_games(games: list[Game]) -> None:
    # Post initial message
    try:
        initial_message = f"I have the analysis for today's games ({date.today().strftime('%Y-%m-%d')})"
        initial_response = post_to_slack(initial_message)
        thread_ts = initial_response['ts']
        logger.info("Posted initial message to Slack")
    except Exception as error:
        raise Exception(f"Failed to post initial message to Slack: {error}")
    
    # Post each game analysis as a thread reply
    for game in games:
        try:
            analysis = analyze_game(game)
        except ValueError:
            raise

        try:
            post_to_slack(analysis, thread_ts=thread_ts)
            logger.info(
                f"""
                Posted analysis for {game.awayTeam.name} @ {game.homeTeam.name}
                """)
        except Exception as error:
            raise Exception(
                f"""
                Failed to post analysis for {game.awayTeam.name} @ {game.homeTeam.name}: {error}
                """
            )

if __name__ == "__main__":
    config = Config() # pyright: ignore[reportCallIssue]

    try:
        schedule = get_tonight_schedule()
    except HTTPError as error:
        logger.error(error)
        exit(1)

    games = parse_schedule(schedule)

    try:
        analyze_and_post_games(games)
    except Exception as error:
        logger.info(error)