# Flask related methods...
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify, send_from_directory, after_this_request, send_file, session, abort, Response
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

# math stuff
from math import floor
from math import ceil

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

# Regular expressions
import re

# Blueprint
mod_api = Blueprint("api", __name__, url_prefix="/api")

def getListOfTimestamps(config):
    tsFiles = os.listdir(config["OUTPUT_FOLDER"])
    timestamps = []
    for file in tsFiles:
        if re.match("[0-9]+\.(mkv|mp4|mpeg4|ts)", file):
            timestamp = file.split(".")[0]
            timestamps.append(timestamp)
    
    timestamps.sort()
    return timestamps

def constructM38UPlaylist(config):
    pass

@mod_api.teardown_request
def teardown(error=None):
    pass

@mod_api.route("/get_min_timestamp/", methods=["POST"])
def get_timestamps_info():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    
    tsFiles = os.listdir(config["OUTPUT_FOLDER"])
    timestamps = []
    for file in tsFiles:
        if re.match("[0-9]+\.(mkv|mp4|mpeg4|ts)", file):
            timestamp = file.split(".")[0]
            timestamps.append(timestamp)
    
    timestamps.sort()

    return jsonify({
        "auth_fail": False,
        "result": {
            "min": timestamps[0],
            "max": timestamps[-1]
        }
    }, 200)

@mod_api.route("/set_start_timestamp/", methods=["POST"])
def set_start_timestamp():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)

    return jsonify({
        "auth_fail": False,
        "result": {
        }
    }, 200)

@mod_api.route("/get_next_m3u8/playlist.m3u8", methods=["GET"])
def get_next_m3u8():
    #if not is_valid_session(request, config):
    #    return abort(403)
       
    if not session.get("last_timestamp", None):
        timestamps = getListOfTimestamps(config)
        if len(timestamps) < config["MAX_SEGMENTS_PER_HLS"]:
            lastTimestamp = timestamps[0]
        else:
            lastTimestamp = timestamps[-10]
        sequence = 0
        session["sequence"] = sequence
        session["last_timestamp"] = lastTimestamp
    else:
        lastTimestamp = session["last_timestamp"]
        sequence = session["sequence"]
        timestamps = getListOfTimestamps(config)
        l = 0
        r = len(timestamps) - 1
        notFound = True
        newIndex = 0
        while l < r and notFound:
            if timestamps[floor((r + l)/2)] <=  lastTimestamp and lastTimestamp < timestamps[floor((r + l)/2) + 1]:
                lastTimestamp = timestamps[floor((r + l)/2) + 1]
                newIndex = floor((r + l)/2) + 1
                notFound = False;
                break;
            if notFound:
                if timestamps[floor((r + l)/2)] <  lastTimestamp:
                    l = floor((r + l) / 2)
                else:
                    r = ceil((r + l) / 2)
        if notFound:
            return abort(404)
        session["last_timestamp"] = lastTimestamp
    
    
    sequence += min(newIndex + config["MAX_SEGMENTS_PER_HLS"], len(timestamps) - 1) - newIndex;
    session["sequence"] = sequence
    durations = [];
    
    for idx in range(newIndex, min(newIndex + config["MAX_SEGMENTS_PER_HLS"], len(timestamps) - 1)):
        vfile = timestamps[idx] + "." + config["VIDEO_CONTAINER"];
        vfile_full_path = config["OUTPUT_FOLDER"] + vfile;
        result=os.popen("".join([config["EXEC_DIR"], "/", config["EXTRACT_DURATION_SCRIPT"], " ", vfile_full_path])).read().strip();
        durations.append(result);
    
    max_duration = max(durations);
    playlist = "#EXTM3U\r\n";
    playlist += "#EXT-X-TARGETDURATION:" + str(max_duration) + "\r\n";
    playlist += "#EXT-X-VERSION:" + str(config["M3U8_VERSION"]) + "\r\n";
    playlist += "#EXT-X-MEDIA-SEQUENCE:" + str(sequence) + "\r\n";
    playlist += "#EXT-X-PROGRAM-DATE-TIME:" + datetime.datetime.fromtimestamp(lastTimestamp).isoformat() + "Z\r\n";

    for i in range(0, len(durations)):
        playlist += "#EXTINF:" + str(durations[i]) + ",\r\n";
        playlist += current_web_path + str(stream_id) + "/" + str(timestamp) + "/" +  str(i + 1) + ".ts\r\n";
    
    resp = Response(response=playlist, status=200,  mimetype="application/x-mpegURL")
    return resp

@mod_api.route("/get_key/", methods=["POST"])
def get_key():
    if not is_valid_session(request, config):
        return jsonify({"auth_fail": True}, 403)
    
    return jsonify({
        "auth_fail": False,
    }, 200)

