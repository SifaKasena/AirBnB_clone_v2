#!/usr/bin/python3
"""
"""
from fabric.api import *
import os

env.hosts = ['18.234.106.203', '54.236.12.250']


def do_clean(number=0):
    """
    Deletes out-of-date archives, both locally and remotely.

    Args:
        number (int): The number of archives to keep. If 0, all archives
                      are deleted except the most recent.

    Returns:
        bool: True if the cleaning was successful, False otherwise.
    """
    try:
        number = int(number)
        if number < 0:
            return False
    except ValueError:
        return False

    if number == 0:
        number = 1

    archives = sorted(os.listdir("versions"))
    for i in range(number):
        archives.pop()

    with lcd("versions"):
        for archive in archives:
            local(f"rm -f {archive}")

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]

        for i in range(number):
            archives.pop()

        for archive in archives:
            run("sudo rm -rf {}".format(archive))

    return True