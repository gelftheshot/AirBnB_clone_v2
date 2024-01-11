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
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


# def do_deploy(archive_path):
#     """
#     Deploys a compressed archive to the web servers

#     Args:
#         archive_path (str): The path to the compressed archive

#     Returns:
#         bool: True if the deployment was successful, False otherwise
#     """
#     if not os.path.exists(archive_path):
#         return False
#     try:
#         file = archive_path.split("/")[-1]
#         name = file.split(".")[0]
#         put(archive_path, "/tmp/{}".format(file))
#         run("rm -rf /data/web_static/releases/{}/".format(name))
#         run("mkdir -p /data/web_static/releases/{}/".format(name))
#         run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
#             .format(file, name))
#         run("rm /tmp/{}".format(file))
#         run("mv /data/web_static/releases/{}/web_static/*/"
#             "data/web_static/releases/{}/"
#             .format(name, name))
#         run("rm -rf /data/web_static/releases/{}/web_static".format(name))
#         run("rm -rf /data/web_static/current")
#         run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
#             .format(name))
#         return True
#     except Exception:
#         return False


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
