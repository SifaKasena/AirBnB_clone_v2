#!/usr/bin/env bash
# This script sets up a web server for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo echo "Test Html" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i '$c\ \n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n}' /etc/nginx/sites-available/default
sudo service nginx restart
