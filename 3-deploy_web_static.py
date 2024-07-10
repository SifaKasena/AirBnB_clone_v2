#!/usr/bin/python3
"""
Fabric script that deploys an archive to your web servers

Usage: fab -f 2-do_deploy_web_static.py do_deploy:<ARCHIVE_PATH>
"""
import os
from datetime import datetime
from fabric.api import local, env, put, run

env.hosts = ['18.234.106.203', '54.236.12.250']

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: The file path of the generated .tgz archive.
             Returns None if an exception occurs during the process.
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(now)
    try:
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Deploys a compressed archive to the web servers.

    Args:
        archive_path (str): The path to the compressed archive.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False
    
    try:
        put(archive_path, "/tmp/")

        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]
        run(f"sudo mkdir -p /data/web_static/releases/{archive_name}/")
        run(f"sudo tar -xzf /tmp/{archive_name}.tgz -C /data/web_static/releases/{archive_name}/")
        run(f"sudo rm -rf /tmp/{archive_name}.tgz")
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -sf /data/web_static/releases/{archive_name} /data/web_static/current")
        return True
    except Exception:
        return False
   
def deploy():
    """
    Deploys the web static content to the web servers.
    
    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    
    return do_deploy(archive_path)
