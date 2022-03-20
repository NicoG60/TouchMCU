from enum import Enum
import importlib.resources

from yaml import load, dump
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

OVERLAYS = "touchmcu.overlays"
SCRIPTS = "touchmcu.scripts"


def load_script(name):
    with importlib.resources.open_text(SCRIPTS, name) as fp:
        data = fp.read()

    return data

def load_all_scripts(*names):
    data = []

    for name in names:
        data.append(load_script(name))

    return '\n\n'.join(data)

def load_overlay(name):
    with importlib.resources.open_text(OVERLAYS, name) as fp:
        data = load(fp.read(), Loader=Loader)

    return data

def list_overlays():
    for name in importlib.resources.contents(OVERLAYS):
        if name.endswith(".yml"):
            yield name