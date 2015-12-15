import os
import pwd
import shutil
import yaml

from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render
from charms.reactive import hook, set_state, when, when_not, remove_state
import gobinary


@hook('install')
def install():
    config = gobinary.config()
    install_workload(config)


@hook('upgrade-charm')
def upgrade():
    # TODO: get_state("go-binary.config")
    #       and compare with upgraded, remove old service if name has changed.
    config = gobinary.config()
    service = config["binary"]
    need_restart = False
    if host.service_running(service):
        need_restart = True
        host.service_stop(service)
    install_workload(config)
    if need_restart:
        host.service_start(service)


@when('gobinary.start')
def restart_gobinary():
    remove_state('gobinary.start')
    bin_config = gobinary.config()
    if host.service_running(bin_config['binary']):
        host.service_restart(bin_config['binary'])
    else:
        host.service_start(bin_config['binary'])
    set_state('gobinary.started')


@when('gobinary.stop')
def stop_gobinary():
    remove_state('gobinary.stop')
    bin_config = gobinary.config()
    if host.service_running(bin_config['binary']):
        host.service_stop(bin_config['binary'])


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
    set_state('go-binary.available')
