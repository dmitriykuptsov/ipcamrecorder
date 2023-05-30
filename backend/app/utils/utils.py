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

import jwt
from Crypto.Hash import SHA256
import datetime

def unique(list):
 
    # initialize a null list
    unique_list = []
 
    # traverse for all elements
    for x in list:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def if_null(value):
    if not value or value == 0:
        return "-"
    else:
        return value

def get_date_formatted(date):
    if date:
        return date.strftime("%Y.%m.%d")
    return ""

def hash_password(password, salt):
    """
    Hashes password
    """
    print("Hashing password and salt")
    print(password)
    print(salt)
    h = SHA256.new()
    h.update(str.encode(password + salt, encoding="UTF-8"))
    c_hashed = h.hexdigest()
    return  bytes(c_hashed, encoding="UTF-8")

def hash_string(data):
    """
    Hashes password
    """
    h = SHA256.new()
    h.update(str.encode(data, encoding="UTF-8"))
    c_hashed = h.hexdigest()
    return c_hashed

def hash_bytes(data):
    """
    Hashes password
    """
    h = SHA256.new()
    h.update(data)
    c_hashed = h.hexdigest()
    return c_hashed

def check_password(password, salt, hashed):
    """
    Checks whether the hashed password matches a give
    hash string
    """
    h = SHA256.new()
    h.update(password + salt)
    c_hashed = h.hexdigest()
    print(hashed)
    print(salt)
    print(c_hashed)
    return  c_hashed == hashed 

def encode_jwt(username, role_id, salt, server_nonce, days, key):
    """
    Create an ecoded JSON token
    """
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=days),
        "iat": datetime.datetime.utcnow(),
        "subject": username,
        "salt": salt,
        "server_nonce": server_nonce,
        "role_id": role_id
    }
    return jwt.encode(
        payload,
        key,
        algorithm='HS256'
    )#.decode("UTF-8")

def decode_jwt(auth_token, key):
    """
    Decodes JSON token and checks its validity
    """
    try:
        return jwt.decode(auth_token, key, algorithms=["HS256"])
    except:
        return {
            "exp": 0,
            "iat": 0,
            "subject": None,
            "salt": None,
            "server_nonce": None,
            "role_id": None
        }

def is_valid_auth_token(auth_token, server_nonce, key):
    """
    Validates the token by first decoding it and
    then checking that the nonce is correct and
    that the exparation time is not in the past
    """
    try:
        payload = jwt.decode(auth_token, key, algorithms=["HS256"])
    except:
        return False
    if payload["server_nonce"] == server_nonce and payload["exp"] >= int(datetime.datetime.utcnow().timestamp()):
        return True
    else:
        return False

def get_auth_token(request):
    """
    Gets the authentication token from the HTTP header
    """
    #return request.headers.get("Authorization", "").replace("Bearer ", "")
    return request.cookies.get("token")

def get_role(request, config):
    """
    Helper utility that gets the token from header and decodes it
    """
    auth_token = get_auth_token(request)
    print("GET ROLE....")
    print(auth_token)
    if auth_token != None and auth_token != "":
        #return is_valid_auth_token(token, config["SERVER_NONCE"], config["TOKEN_KEY"])
        try:
            payload = jwt.decode(auth_token, config["TOKEN_KEY"], algorithms=["HS256"])
            
            print(payload)
            return payload["role_id"]
        except Exception as e:
            print(e)
            return None
    return None

def get_subject(request, config):
    auth_token = get_auth_token(request)
    print("GET ROLE....")
    print(auth_token)
    if auth_token != None and auth_token != "":
        #return is_valid_auth_token(token, config["SERVER_NONCE"], config["TOKEN_KEY"])
        try:
            payload = jwt.decode(auth_token, config["TOKEN_KEY"], algorithms=["HS256"])
            print(payload)
            return payload["subject"]
        except Exception as e:
            print(e)
            return None
    return None

def is_valid_session(request, config):
    """
    Helper utility that gets the token from header
    and checks wether it is valid one
    """
    token = get_auth_token(request)
    if token != None and token != "":
        return is_valid_auth_token(token, config["SERVER_NONCE"], config["TOKEN_KEY"])
    return False
