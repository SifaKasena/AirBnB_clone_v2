#!/usr/bin/python3
from fabric.api import local
from time import strftime
from datetime import date
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    time_str = strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(time_str)
    print("Packing web_static to {}".format(archive_path))
    try:
        local("mkdir -p versions")
        output = local("tar -czvf {} web_static/".format(archive_path))
        if output.failed:
            return None

        size = os.path.getsize(archive_path)
        print("web_static packed: {} -> {}Bytes".format(archive_path, size))
        return archive_path
    except Exception as e:
        return None
