from flask import Flask, request, render_template
import requests
import google.auth
import google.auth.transport.requests

# Initialize Flask app
app = Flask(__name__)
project_number = "813347764116"
location = "us"
app_id = "nhl_1740610249096"

url = f"https://us-discoveryengine.googleapis.com/v1alpha/projects/{project_number}/locations/{location}/collections/default_collection/engines/{app_id}/servingConfigs/default_search:search"
        
@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Get the user's query from the form
        query = request.form['query']
        
        # Get the access token using google.auth
        creds, _ = google.auth.default()
        creds.refresh(google.auth.transport.requests.Request())
        access_token = creds.token
    
        # Set up the headers
        headers = {
          "Authorization": f"Bearer {access_token}",
          "Content-Type": "application/json"
        }
        
        # Set up the JSON payload
        payload = {
          "query": query,
          "pageSize": 10,
          "queryExpansionSpec": {"condition": "AUTO"},
          "spellCorrectionSpec": {"mode": "AUTO"}
        }
        
        # Send the POST request using requests
        response = requests.post(url, headers=headers, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Extract results (assuming 'results' key; adjust if needed)
            results = []
            for result in data.get('results', []):
              # Extract title and snippet from structData (adjust fields as needed)
              struct_data = result.get('document', {}).get('structData', {})
              away_team = struct_data.get('away_team')
              home_team = struct_data.get('home_team')
              date = struct_data.get('date')
              time = struct_data.get('time')
              away_team_score = struct_data.get('away_team_score')
              home_team_score = struct_data.get('home_team_score')
              results.append(
                {
                  'away_team': away_team,
                  'home_team': home_team,
                  'date': date,
                  'time': time,
                  'away_team_score': away_team_score,
                  'home_team_score': home_team_score
                }
              )
            
            # Render the template with search results
            return render_template('search.html', results=results)
        else:
            error_message = f"Error: {response.status_code} - {response.text}"
            return render_template('search.html', results=[], error=error_message)
    else:
        # For GET request, render the template with no results
        return render_template('search.html', results=[])

if __name__ == '__main__':
    app.run(debug=True)