# Flask related methods...
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, send_from_directory, after_this_request, send_file
# Secure filename
from werkzeug.utils import secure_filename

# importing os module
import os

# System libraries
from datetime import datetime
# Regular expressions libraries
import re

# Trace back libary
import traceback

# Configuration
from app import config_ as config

# Security helpers
from app.utils.utils import is_valid_session, hash_password, get_subject
from app.utils.utils import get_role
from app.utils.utils import hash_string
from app.utils.utils import hash_bytes

# Datetime utilities
from datetime import date

# Threading stuff
from time import sleep
import threading

# Logging 
import logging

# OS and representation stuff
import os
from binascii import hexlify

# Temporary files
import tempfile

# Security stuff
from Crypto.Hash import SHA256


# Blueprint
mod_api = Blueprint("api", __name__, url_prefix="/api")


@mod_api.teardown_request
def teardown(error=None):
    pass

@mod_api.route("/get_min_timestamp/", methods=["POST"])
def get_min_timestamp():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    
    return jsonify({
        "auth_fail": False,
    }, 200)

@mod_api.route("/get_next_m3u8/", methods=["POST"])
def get_next_m3u8():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    
    return jsonify({
        "auth_fail": False,
    }, 200)

@mod_api.route("/get_key/", methods=["POST"])
def get_key():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    
    return jsonify({
        "auth_fail": False,
    }, 200)

