from flask import Flask, request, render_template
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine

project_id = "proj-goldeneye-59465"
location = "us"
engine_id = "nhl_1740610249096"

# Initialize Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
  if request.method == 'POST':
    # Get the user's query from the form
    query = request.form['query']

    # Call the function to answer the query
    response = answer_query_sample(project_id, location, engine_id, query)

    data = response.json()

    # Extract results (assuming 'results' key; adjust if needed)
    results = []
    for result in data.get('results', []):
        # print (result)
        # Extract title and snippet from structData (adjust fields as needed)
        struct_data = result.get('document', {}).get('structData', {})
        away_team = struct_data.get('away_team')
        home_team = struct_data.get('home_team')
        date = struct_data.get('date')
        time = struct_data.get('time')
        away_team_score = struct_data.get('away_team_score')
        home_team_score = struct_data.get('home_team_score')
        results.append({'away_team': away_team, 'home_team': home_team, 'date': date, 'time': time, 'away_team_score': away_team_score, 'home_team_score': home_team_score})
    
    # Render the template with search results
    return render_template('search.html', results=results)
  else:
      # For GET request, render the template with no results
      return render_template('search.html', results=[])
  
def answer_query_sample(
    project_id: str,
    location: str,
    engine_id: str,
    query: str,
) -> discoveryengine.AnswerQueryResponse:
    #  For more information, refer to:
    # https://cloud.google.com/generative-ai-app-builder/docs/locations#specify_a_multi-region_for_your_data_store
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    # Create a client
    client = discoveryengine.ConversationalSearchServiceClient(
        client_options=client_options
    )

    # The full resource name of the Search serving config
    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_serving_config"

  # Initialize request argument(s)
    request = discoveryengine.AnswerQueryRequest(
        serving_config=serving_config,
        query=discoveryengine.Query(text=query),
        session=None,  # Optional: include previous session ID to continue a conversation
    )

    # Make the request
    response = client.answer_query(request)

    # # Handle the response
    # print(response)

    return response

if __name__ == '__main__':
    app.run(debug=True)