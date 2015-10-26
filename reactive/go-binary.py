import os
import pwd
import shutil
import yaml

from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render
from charms.reactive import hook
from charms.reactive.bus import get_states


@hook('install')
def install():
    install_workload()


@hook('upgrade-charm')
def upgrade():
    charm_dir = hookenv.charm_dir()
    with open(os.path.join(charm_dir, "go-binary.yaml")) as f:
        go_binary = yaml.load(f)
        service = go_binary["binary"]
        need_restart = False
        if host.service_running(service):
            need_restart = True
        if need_restart:
            host.service_stop(service)
        install_workload()
        if need_restart:
            host.service_start(service)


def install_workload():
    charm_dir = hookenv.charm_dir()
    with open(os.path.join(charm_dir, "go-binary.yaml")) as f:
        go_binary = yaml.load(f)
        local_binary = os.path.join(charm_dir, "files", go_binary["binary"])
        install_binary = "/usr/bin/" + go_binary["binary"]
        args = go_binary["args"]
        shutil.copyfile(local_binary, installed_binary)
        render(source="upstart",
            target="/etc/init/%s.conf" % (binary_name),
            owner="root",
            perms=0o644,
            context={
                "ctx": go_binary,
                "install_binary": "install_binary",
            })
