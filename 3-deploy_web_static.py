#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy
"""

import os.path
from fabric.api import env, put, run, local
from datetime import datetime

env.hosts = ['100.26.49.67', '34.201.61.34']


def do_pack():
    """
    Creates a compressed archive of the web_static folder.

    Returns:
        str: The file path of the compressed archive.
             Returns None if the archive creation fails.
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        path = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(path))
        return path
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploys a compressed archive to the web servers

    Args:
        archive_path (str): The path to the compressed archive

    Returns:
        bool: True if the deployment was successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False
    try:
        file = archive_path.split("/")[-1]
        name = file.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}{}/".format(path, name))
        run("sudo tar -xzf /tmp/{} -C {}{}/".format(file, path, name))
        run("sudo rm /tmp/{}".format(file))
        run("sudo mv {0}{1}/web_static/* {0}{1}/".format(path, name))
        run("sudo rm -rf {}{}/web_static".format(path, name))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}{}/ /data/web_static/current".format(path, name))
        return True
    except Exception:
        return False


def deploy():
    """
    Deploys the web static content by calling the
    do_pack and do_deploy functions.

    Returns:
        bool: True if the deployment is successful, False otherwise.
    """
    try:
        path = do_pack()
        return do_deploy(path)
    except Exception:
        return False
