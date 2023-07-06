#!/usr/bin/python3
"""This script distributes an archive to web servers

Usage: fab -f 2-do_deploy_web_static.py do_deploy<ARCHIVE> <SSH KEY>
"""
from fabric.api import *
from datetime import datetime
import os


env.hosts = ['54.157.179.66', '54.236.28.100']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """
    Deploy web files to server
    """
    try:
        if not (os.path.exists(archive_path)):
            return False

        # Upload archive to /tmp/ path on web server
        put(archive_path, '/tmp/')

        # Get the archive name
        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]

        # Create target directory for deployment
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(archive_name))

        # Extract the uploaded archive.tgz file
        run('sudo tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'.
            format(archive_name, archive_name))

        # Delete the uploaded tgz archive
        run('sudo rm /tmp/{}.tgz'.format(archive_name))

        # Move the contents of the extracted folder to the parent directory
        run('sudo mv /data/web_static/releases/{}/web_static/*\
         /data/web_static/releases/{}/'.
            format(archive_name, archive_name))

        # Delete empty web_static folder
        run('sudo rm -rf /data/web_static/releases/{}/web_static'
            .format(archive_name))

        # Delete the current symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Create new symbolic link
        run('sudo ln -s /data/web_static/releases/{}/\
         /data/web_static/current'.
            format(archive_name))
    except Exception:
        return False
    return True
