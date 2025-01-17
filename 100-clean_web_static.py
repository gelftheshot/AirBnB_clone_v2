#!/usr/bin/python3
"""
Fabric script (based on the file 3-deploy_web_static.py)
that deletes out-of-date archives, using the function do_clean
"""
import os
from fabric.api import *


env.hosts = ['100.26.49.67', '34.201.61.34']


def do_clean(number=0):
    """
    Cleans up old versions of the web static files.

    Args:
        number (int): The number of versions to keep.
        If set to 0, all versions except the latest will be removed.

    Returns:
        None
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
