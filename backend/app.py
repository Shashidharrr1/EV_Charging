from flask import Flask
from flask_cors import CORS
from backend.api import api_bp  # Update import path

app = Flask(__name__)
CORS(app)

# Register the main API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)