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

config = {
    "SEGMENT_DURATION": 10,
    "VIDEO_CONTAINER": "mp4",
    "CAMERA_NAME": "CAMERA1",
    "CAMERA_IP_ADDRESS": "192.168.1.21",
    "TRANSPORT_PROTOCOL": "tcp",
    "RTSP_URL": "rtsp://admin:admin@192.168.1.21:554/media/video1",
    "OUTPUT_FOLDER": "/opt/data2/ipcam/storage/192.168.1.21/video1/",
    "CLEAN_UP_SCRIPT": "/opt/data2/ipcam/scripts/cleanup.py",
    "MAX_VIDEO_LIFETIME": 86400,
    "CLEAN_UP_INTERVAL": 60,
    "MPEGTS_UDP_IP": "127.0.0.1",
    "MPEGTS_UDP_PORT": 9000,
    "MPEGTS_PACKET_SIZE": 188,
    "VALID_CHANNEL": 1,
    "SEQUENCE_LENGTH_IN_BYTES": 1*1024*1024,
    "EXEC_DIR": "/opt/data2/ipcam/scripts/",
    "CONVERT_RAW_TS": "convert_ts.sh"
}
