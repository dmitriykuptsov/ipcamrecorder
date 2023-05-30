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

__author__ = "Dmitriy Kuptsov"
__copyright__ = "Copyright 2023, stangebit"
__license__ = "GPL"
__version__ = "0.0.1a"
__maintainer__ = "Dmitriy Kuptsov"
__email__ = "dmitriy.kuptsov@gmail.com"
__status__ = "development"

# Logging
import logging

# import system library
import sys

# Configuration
from config import config

# Threading
import threading

# Errors
import traceback

# Timing
from time import sleep

# Import OS stuff
import os

# Regular expressions
import re

# Subprocesses
import subprocess

# Datetime stuff
from datetime import datetime

# Configure logging to console and file
logging.basicConfig(
	level=logging.DEBUG,
	format="%(asctime)s [%(levelname)s] %(message)s",
	handlers=[
		logging.FileHandler("rtsp_capture.log"),
		logging.StreamHandler(sys.stdout)
	]
);

def capturing(config):
    """
    Captures the stream, slices it and writes to the disk
    """

    while True:
        folder = config["OUTPUT_FOLDER"]
        if not os.path.exists(config["OUTPUT_FOLDER"]):
            os.makedirs(folder)
        try:
            subprocess.run(["ffmpeg", \
                    "-i", \
		    config["RTSP_URL"], \
                    "-rtsp_transport", \
		    config["TRANSPORT_PROTOCOL"], \
                    "-vcodec", "copy", \
		    "-acodec", "copy", \
                    "-f", "segment", \
                    "-reset_timestamps", "1", \
                    "-segment_time", str(config["SEGMENT_DURATION"]), \
                    "-segment_format", config["VIDEO_CONTAINER"], \
                    "-strftime", "1",  folder + "%s." + config["VIDEO_CONTAINER"] \
                    ])
        except Exception as e:
            logging.critical("Exception occured while capturing the video stream ....!!!!")
            logging.critical(e);
            traceback.print_exc()
        logging.debug("Capturing process died, restarting the ffmpeg process")
        sleep(10)

def cleanup(config):
    """
    Cleans up old MP4 files
    """
    while True:
        try:
            if os.path.exists(config["OUTPUT_FOLDER"]):
                files = os.listdir(config["OUTPUT_FOLDER"])
                now = int(datetime.now().timestamp())
                for file in files:
                    if re.match("[0-9]+\.(mp4|mpeg4|mkv|avi)", file):
                        ts = int(file.split(".")[0])
                        if ts <= now - int(config["MAX_VIDEO_LIFETIME"]):
                            logging.debug("Removing the file")
                            os.remove(file)
        except Exception as e:
            logging.critical("Exception occured while removing the file... !!!")
            logging.critical(e);
        sleep(config["CLEAN_UP_INTERVAL"])

capture_loop = threading.Thread(target = capturing, args = (config, ), daemon = True);
capture_loop.start()

clean_loop = threading.Thread(target = cleanup, args = (config, ), daemon = True);
clean_loop.start()

main_loop = True;

while main_loop:
    logging.debug("Running RTSP stream capturing application");
    sleep(10)
