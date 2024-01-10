#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
"""
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """
    Creates a compressed archive of the web_static folder.

    Returns:
        str: The file path of the compressed archive.
             Returns None if the archive creation fails.
    """
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(date)
    try:
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(file))
        return file
    except Exception:
        return None
