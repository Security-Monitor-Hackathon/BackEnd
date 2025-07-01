import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from routes.auth_routes import auth_bp
from routes.pipeline_routes import pipeline_bp
from routes.map_routes import map_bp


app = Flask(__name__)

    
app.register_blueprint(auth_bp)
app.register_blueprint(pipeline_bp)
app.register_blueprint(map_bp)

@app.route('/')
def home():
    return 'Hello, World!'