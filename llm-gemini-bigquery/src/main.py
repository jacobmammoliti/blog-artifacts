import os
import sys
from typing import Callable
from langchain_google_vertexai import ChatVertexAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from slack_bolt import App

try:
    database_uri = os.environ['DATABASE_URI']
    slack_bot_token = os.environ['SLACK_BOT_TOKEN']
except KeyError as error:
    sys.exit(f"Failed to get required environment variable {error}.")

llm_model = os.getenv('MODEL', 'gemini-1.5-flash')
verbose_mode = os.getenv('VERBOSE', True)
socket_mode = os.getenv('SOCKET_MODE', False)

if socket_mode:
    from slack_bolt.adapter.socket_mode import SocketModeHandler

    try:
        slack_app_token = os.environ['SLACK_APP_TOKEN']
    except KeyError:
        sys.exit(f"Failed to get required environment variable SLACK_APP_TOKEN.")
    
    # Initializes app with bot token only. App token is passed when we call the handler
    app = App(token=slack_bot_token)
else:
    slack_signing_secret = os.getenv('SLACK_SIGNING_SECRET', None)

    # Initializes app with bot token and signing secret
    app = App(token=slack_bot_token, signing_secret=slack_signing_secret)

db = SQLDatabase.from_uri(database_uri)
llm = ChatVertexAI(model=llm_model)

agent_executer = create_sql_agent(
    llm=llm,
    db=db,
    verbose=verbose_mode,
    agent_type="zero-shot-react-description",
    agent_executor_kwargs={"return_intermediate_steps": True}
)

@app.event("app_mention")
def mention_handler(body: dict, say: Callable):
    question = body['event']['blocks'][0]['elements'][0]['elements'][1]['text']
    
    # Send question to SQL agent
    response = agent_executer.invoke(question)
    print(response['intermediate_steps'])
    say(response['output'])

if __name__ == "__main__":
    if socket_mode:
        SocketModeHandler(app, slack_app_token).start()
    else:
        app.start(port=int(os.environ.get("PORT", 3000)))