#!/usr/bin/python3

# Copyright (C) 2019 strangebit

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify

# Import password / encryption helper tools
#from werkzeug.security import generate_password_hash, check_password_hash

import os
from binascii import hexlify

# Import the database object from the main app module
#from app import config
import app
from app import config_

# Secrets
import secrets

# Password encryption routines
#import crypt

# Import regex stuff
import re

from app.utils.utils import check_password, encode_jwt, is_valid_auth_token, get_auth_token, decode_jwt

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route("/signin/", methods=["POST"])
def signin():
    if request.method == "POST":
        data = request.get_json(force=True)
        if not data:
            return jsonify({
                "success": False
            }, 200)
        salt = hexlify(os.urandom(32))

        print("Login into the system")
        print("Username : " + data.get("username", ""))
        print("Password : " + data.get("password", ""))
        if data.get("username", "") == config_["USER"] \
            and check_password(data.get("password", "").encode("UTF-8"), config_["SALT"].encode("UTF-8"), config_["PASSWORD"]):
            token = encode_jwt(data.get("username", ""), \
                "ADMIN", salt.decode("UTF-8"), config_["SERVER_NONCE"], \
                config_["JWT_VALIDITY_IN_DAYS"], \
                config_["TOKEN_KEY"])
            resp = jsonify({
                "token": token,
                "success": True
            }, 200)
            resp.set_cookie("token", value=token, httponly = True)
            return resp
        else:
            return jsonify({
                "success": False
            }, 200)

@mod_auth.route("/logout/", methods=["GET"])
def logout():
    resp = jsonify({
        "success": True
    }, 200)
    resp.set_cookie("token", value=None)
    return resp

@mod_auth.route("/validate_token/", methods=["POST"])
def validate_token():
    token = get_auth_token(request)
    return jsonify({
        "valid": is_valid_auth_token(token, config_["SERVER_NONCE"], config_["TOKEN_KEY"])
    }, 200)
