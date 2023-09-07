from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.utilities import SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits.sql.prompt import SQL_PREFIX

dataset = input("Enter the dataset URI: ")
prompt = input("Enter the prompt: ")
verbose = input("Run in verbose mode? ")

# https://api.python.langchain.com/en/latest/utilities/langchain.utilities.sql_database.SQLDatabase.html
db = SQLDatabase.from_uri(dataset) # uses SQLAlchemy's create_engine() function under the hood
llm = ChatOpenAI(temperature=0, model_name='gpt-4', verbose=verbose)

# https://api.python.langchain.com/en/latest/_modules/langchain/agents/agent_toolkits/sql/base.html#create_sql_agent
agent_executor = create_sql_agent(
  llm=llm,
  toolkit=SQLDatabaseToolkit(db=db, llm=llm),
  verbose=verbose,
  agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
  prefix=SQL_PREFIX
)

output = agent_executor.run(prompt)

print (output)