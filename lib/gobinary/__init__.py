import os
import yaml

from charmhelpers.core import hookenv


def config():
    with open(os.path.join(hookenv.charm_dir(), "go-binary.yaml")) as f:
        return yaml.load(f)
