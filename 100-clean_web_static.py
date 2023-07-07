#!/usr/bin/python3
"""This script deletes out-of-date archives

Usage: fab -f 100-clean_web_static.py do_clean:number=<NUMBER>
If number is 0 or 1, keep only the most recent version of archive.
if number is 2, keep the most recent, and 2nd most recent archive.
"""
import os
from fabric.api import *

env.hosts = ['54.157.179.66', '54.236.28.100']


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number (int): The number of archives to keep.
    """
    if int(number) == 0:
        number = 1
    else:
        number = int(number)

    files = sorted(os.listdir("versions"))
    for i in range(number):
        files.pop()

    with lcd("versions"):
        for file in files:
            local("rm ./{}".format(file))

    with cd("/data/web_static/releases"):
        folders = run("ls -tr").split()
        filtered_folders = []
        for folder in folders:
            if "web_static_" in folder:
                filtered_folders.append(folder)
        folders = filtered_folders

        for i in range(number):
            folders.pop()

        for folder in folders:
            run("rm -rf ./{}".format(folder))
