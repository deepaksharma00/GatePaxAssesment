from flask import Flask, jsonify

# Create the Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def read_root():
    """
    Root endpoint to return a simple JSON response.
    """
    return jsonify({"message": "Hello from Flask with Google Functions Framework and Hot-Reloading!"})

# The Functions Framework requires a target function
def handler(request):
    """
    Target function for the Google Functions Framework.
    """
    return app(request.environ, start_response=lambda *args: None)
