#!/usr/bin/python3
"""
This script generates a .tgz archive from web_static folder

Usage: fab -f 1-pack_web_static.py do_pack
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: The file path of the generated .tgz archive.
             Returns None if an exception occurs during the process.
    """
    try:
        local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"versions/web_static_{date}.tgz"
        local(f"tar -cvzf {file_name} web_static")
        return file_name
    except Exception as e:
        return None
