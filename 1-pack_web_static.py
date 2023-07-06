#!/usr/bin/python3
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    time_str = strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(time_str)
    try:
        local("mkdir -p versions")
        local("tar -czvf {} web_static/".format(archive_path))
        return archive_path
    except Exception as e:
        return None
