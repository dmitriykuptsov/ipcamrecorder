# Import flask and template operators
from flask import Flask, render_template, redirect, url_for

# System libraries
import os
import re
import secrets
from datetime import datetime

from flask_cors import CORS

# Define the WSGI application object
app = Flask(__name__, static_folder = 'templates/static')

# Allow Cross origin requests
cors = CORS(app, resources={r"*": {"origins": "*"}})

# Configurations
app.config.from_object('config')

config_ = app.config;

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404

@app.route("/")
def index():
	return redirect(url_for("auth.signin"))

# Import a module / component using its blueprint handler variable
from app.auth.controllers import mod_auth
from app.api.controllers import mod_api

# Register blueprint(s)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_api)

