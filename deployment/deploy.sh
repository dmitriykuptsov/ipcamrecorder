#!/bin/bash
sudo apt-get update
sudo apt-get install nginx
sudo apt-get install ffmpeg
sudo apt-get install python3
sudo apt-get install python3-pip

sudo pip3 install flask
sudo pip3 install flask_cors
sudo pip3 install pycryptodome
sudo pip3 install logging

echo "Creating application folders"
sudo mkdir -p /opt/data2/ipcam/hls/
sudo mkdir -p /opt/data2/ipcam/capture/
sudo mkdir -p /opt/data2/ipcam/storage/192.168.1.21/video1

sudo chown www-data:www-data -R /opt/data2/ipcam/
sudo chown www-data:www-data -R /opt/data2/ipcam/capture/
sudo chown www-data:www-data -R /opt/data2/ipcam/hls/

echo "Copying Nginx configuration files"
sudo rsunc -rv ../streaming/default /etc/ngnix/site-available/default
sudo ln -s /etc/nginx/site-available/default /etc/nginx/sites-enabled/default
sudo service nginx restart

echo "Copying the Flask application"
sudo rsync -rv ../backend/app ../backend/run.py ../backend/config.py /opt/data2/ipcam/hls/
sudo chown www-data:www-data -R /opt/data2/ipcam/hls/

echo "Copying the RTSP stream capture application"
sudo rsync -rv ../capture/* /opt/data2/ipcam/capture/
sudo chown www-data:www-data -R /opt/data2/ipcam/capture/

echo "Copying the web application files"
sudo rsync -rv ../frontend/nvr/dist/* /var/www/html/ipcam/

echo "Copying and enabling the service files"
sudo rsync -rv ../startup/rtsp-capture.service /etc/systemd/system/
sudo systemctl enable rtsp-capture
sudo systemctl start rtsp-capture

sudo rsync -rv ../startup/hls-ipcam.service /etc/systemd/system/
sudo systemctl enable hls-ipcam
sudo systemctl start hls-ipcam
