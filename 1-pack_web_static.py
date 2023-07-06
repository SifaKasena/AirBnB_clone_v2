#!/usr/bin/python3
"""This script generates a .tgz archive from web_static folder

Usage: fab -f 1-pack_web_static.py do_pack
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    now = datetime.now()
    archive_path = "versions/web_static_{}{}{}{}{}{}.tgz".format(now.year,
                                                                 now.month,
                                                                 now.day,
                                                                 now.hour,
                                                                 now.minute,
                                                                 now.second)
    print("Packing web_static to {}".format(archive_path))
    try:
        local("mkdir -p versions")
        output = local("tar -czvf {} web_static/".format(archive_path))
        if output.succeeded:
            size = os.path.getsize(archive_path)
            print("web_static packed: {} -> {}Bytes".
                  format(archive_path, size))
            return archive_path
        return None

    except Exception as e:
        return None
