import os
from flask_restful import Api
from flask_cors import CORS
from flask import Flask

if os.path.exists("env.py"):
    import env

# Instantiate Flask App
app = Flask(__name__)
CORS(app)

# Set app Paramteres
app.secret_key = os.environ.get("SECRET_KEY")

# Define API
api = Api(app)