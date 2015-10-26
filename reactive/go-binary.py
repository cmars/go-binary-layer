import os
import pwd
import shutil
import yaml

from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render
from charms.reactive import hook, set_state
import gobinary


@hook('install')
def install():
    config = gobinary.config()
    install_workload(config)
    set_state('%s.available' % (config['binary']))


@hook('upgrade-charm')
def upgrade():
    # TODO: get_state("go-binary.config")
    #       and compare with upgraded, remove old service if name has changed.
    config = gobinary.config()
    service = config["binary"]
    need_restart = False
    if host.service_running(service):
        need_restart = True
    if need_restart:
        host.service_stop(service)
    install_workload(config)
    if need_restart:
        host.service_start(service)


def install_workload(config):
    local_binary = os.path.join(hookenv.charm_dir(), "files", config["binary"])
    install_binary = "/usr/bin/" + config["binary"]
    args = config["args"]
    shutil.copyfile(local_binary, install_binary)
    os.chmod(install_binary, 0o755)
    render(source="upstart",
        target="/etc/init/%s.conf" % (config["binary"]),
        owner="root",
        perms=0o644,
        context={
            "ctx": config,
            "install_binary": install_binary,
        })
    set_state('go-binary.config' % (config))
