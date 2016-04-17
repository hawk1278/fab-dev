#!/usr/bin/env python
import os

from fabric.api import *
from fabric.contrib.files import is_link, exists
from fabtools import git
from fabtools.files import symlink
from fabtools import supervisor
from fabtools.require import rpm, directory
from fabtools.python import virtualenv, install
import time

local_config_dir = "./config"
remote_config_dir = "/etc/supervisor.d"
app_dir = "/opt/router_log_parser"
app_repo = "https://github.com/hawk1278/router_log_parser.git"
now = time.strftime("%d-%m-%Y-%H-%M-%S", time.gmtime())
pkg_list = ['python-pip','git','python-virtualenv']
env.roledefs = {
    'appserver':['192.168.1.22']
}
env.warn_only = True
env.ssh_config = True


def clone_repo():
    with cd(app_dir):
        sudo("git clone {0} {1}".format(app_repo, now))


def create_link():
    with cd(app_dir):
        if is_link(os.path.join(app_dir, "current")):
            sudo("rm -f {0}".format(os.path.join(app_dir, "current")))
        symlink(os.path.join(app_dir, now), "current", use_sudo=True)


def configure_supervisor():
    directory(remote_config_dir, use_sudo=True)
    if exists(os.path.join(remote_config_dir, "router_log_parser.conf")) is False:
        with lcd(local_config_dir):
            with cd(remote_config_dir):
                put("./router_log_parser.conf", "./", use_sudo=True)
                supervisor.update_config()


def create_venv():
    with cd(os.path(now,"current")):
        sudo("virtualenv router_log_parser_env")
        with virtualenv("router_log_parser_env"):
            install("pymongo")


def install_reqs():
    for pkg in pkg_list:
        rpm.install(pkg, options="--quiet")
    sudo('pip install supervisor')


@task
def deploy(default=True):
    pass


def run_app():
    pass
