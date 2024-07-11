#!/usr/bin/python3
"""
Fabric script that deploys an archive to your web servers

Usage: fab -f 2-do_deploy_web_static.py do_deploy:<ARCHIVE_PATH>
"""
import os
from fabric.api import env, put, run

env.hosts = ['18.234.106.203', '54.236.12.250']


def do_deploy(archive_path):
    """
    Deploys a compressed archive to the web servers.

    Args:
        archive_path (str): The path to the compressed archive.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """
    try:
        if not os.path.exists(archive_path):
            return False

        put(archive_path, "/tmp/")

        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]

        run(f"sudo mkdir -p /data/web_static/releases/{archive_name}/")
        run(f"sudo tar -xzf /tmp/{archive_name}.tgz -C\
            /data/web_static/releases/{archive_name}/")
        run(f"sudo rm -rf /tmp/{archive_name}.tgz")
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -sf /data/web_static/releases/{archive_name}\
            /data/web_static/current")

    except Exception:
        return False

    return True
