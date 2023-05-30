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
    #print(config["OUTPUT_FOLDER"])
    tsFiles = os.listdir(config["OUTPUT_FOLDER"])
    timestamps = []
    for file in tsFiles:
        if re.match("[0-9]+\." + config["VIDEO_CONTAINER"], file):
            timestamp = file.split(".")[0]
            timestamps.append(int(timestamp))
    
    timestamps.sort()
    return timestamps

@mod_api.teardown_request
def teardown(error=None):
    pass

@mod_api.route("/get_timestamp_range/", methods=["POST"])
def get_timestamps_info():
    #if not is_valid_session(request, config):
    #    return jsonify({"auth_fail": True}, 403)
    
    tsFiles = os.listdir(config["OUTPUT_FOLDER"])
    timestamps = []
    for file in tsFiles:
        if re.match("[0-9]+\." + config["VIDEO_CONTAINER"], file):
            timestamp = file.split(".")[0]
            timestamps.append(int(timestamp))
    
    timestamps.sort()

    if len(timestamps) > 1
        return jsonify({
            "auth_fail": False,
            "result": {
                "min": timestamps[0],
                "max": timestamps[-1],
                "step": (timestamps[1] - timestamps[0])
            }
        }, 200)
    else:
        return jsonify({
            "auth_fail": False,
            "result": {
                "min": None,
                "max": None,
                "step": 0
            }
        }, 200)

@mod_api.route("/get_step/", methods = ["POST"])
def get_step():
    #if not is_valid_session(request, config):
    #    return jsonify({"auth_fail": True}, 403)
    timestamps = getListOfTimestamps(config)

    if len(timestamps) > 1:
        return jsonify({
            "auth_fail": False,
            "result": {
                "diff": (timestamps[1] - timestamps[0])
            }
        }, 200)
    else:
        return jsonify({
            "auth_fail": False,
            "result": {
                "diff": 0
            }
        }, 200)

@mod_api.route("/set_timestamp/<int:timestamp>", methods = ["POST"])
def set_timestamp(timestamp):
    #if not is_valid_session(request, config):
    #    return jsonify({"auth_fail": True}, 403)
    timestamps = getListOfTimestamps(config)
    if timestamp < timestamps[0] or timestamp > timestamps[-1]:
        return jsonify({"auth_fail": False, "result": False, "reason": "Timestamp is out of range"}, 404)
    session["sequence"] = 0
    session["last_timestamp"] = timestamp
    return jsonify({
        "auth_fail": False,
        "result": True
    }, 200)

@mod_api.route("/get_file/<file>", methods=["GET"])
def get_file(file):
    #if not re.match("[0-9]+.(ts|mp4|mkv|mpeg4)", file):
    #    return jsonify({"auth_fail": True}, 403)
    if not re.match("^[0-9]+.(ts|mkv|mp4|mpeg4)$", file):
        return jsonify({"auth_fail": True}, 404)
    filename = config["OUTPUT_FOLDER"] + "/" + file;
    return send_file(filename, mimetype='video/mpegts');

@mod_api.route("/get_next_m3u8/playlist.m3u8", methods=["GET"])
def get_next_m3u8():
    #if not is_valid_session(request, config):
    #    return abort(403)
    newIndex = 0

    if not session.get("last_timestamp", None):
        timestamps = getListOfTimestamps(config)
        if len(timestamps) < config["MAX_SEGMENTS_PER_HLS"]:
            lastTimestamp = int(timestamps[0])
        else:
            lastTimestamp = int(timestamps[-10])
        sequence = 0
        session["sequence"] = sequence
        session["last_timestamp"] = int(lastTimestamp)
    else:
        lastTimestamp = int(session["last_timestamp"])
        sequence = session["sequence"]
        timestamps = getListOfTimestamps(config)

        if session.get("last_timestamp", None) < timestamps[0] or session.get("last_timestamp", None) > timestamps[-1]:
            if len(timestamps) < config["MAX_SEGMENTS_PER_HLS"]:
                lastTimestamp = int(timestamps[0])
            else:
                lastTimestamp = int(timestamps[-10])
            sequence = 0
            session["sequence"] = sequence
            session["last_timestamp"] = int(lastTimestamp)
        else:
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
                        r = floor((r + l) / 2)
            if notFound:
                return Response(response=None, status=404,  mimetype="plain/text")
            session["last_timestamp"] = lastTimestamp
    
    print("Building the file list")
    sequence += min(config["MAX_SEGMENTS_PER_HLS"], len(timestamps));
    session["sequence"] = sequence
    durations = [];
    timestampsToAdd = []
    for idx in range(newIndex, min(newIndex + config["MAX_SEGMENTS_PER_HLS"], newIndex + len(timestamps))):
        vfile = str(timestamps[idx]) + "." + config["VIDEO_CONTAINER"];
        vfile_full_path = config["OUTPUT_FOLDER"] + vfile;
        result=os.popen("".join([config["EXEC_DIR"], "/", config["EXTRACT_DURATION_SCRIPT"], " ", vfile_full_path])).read().strip();
        durations.append(result);
        timestampsToAdd.append(timestamps[idx])
    
    max_duration = max(durations);
    playlist = "#EXTM3U\r\n";
    playlist += "#EXT-X-TARGETDURATION:" + str(max_duration) + "\r\n";
    playlist += "#EXT-X-VERSION:" + str(config["M3U8_VERSION"]) + "\r\n";
    playlist += "#EXT-X-MEDIA-SEQUENCE:" + str(sequence) + "\r\n";
    playlist += "#EXT-X-PROGRAM-DATE-TIME:" + datetime.fromtimestamp(lastTimestamp).isoformat() + "Z\r\n";

    for i in range(0, len(durations)):
        playlist += "#EXTINF:" + str(durations[i]) + ",\r\n";
        playlist += "/api/get_file/" + str(timestampsToAdd[i]) + "." + config["VIDEO_CONTAINER"] + "\r\n";
    
    return Response(response=playlist, status=200,  mimetype="application/x-mpegurl")

