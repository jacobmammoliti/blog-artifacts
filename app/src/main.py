from flask import Flask, render_template

app = Flask(__name__)

# Define index endpoint
@app.route("/")
def index():
    return render_template('index.html')

# Define health endpoint
@app.route('/healthz', methods=['GET'])
def health():
    return 'All good.', 200
 
# Main driver function
if __name__ == "__main__":
    app.run()