import os
import sys
import shutil
import tempfile
import contextlib
from StringIO import StringIO

import pyblish
import pyblish.cli
import pyblish.plugin

config = pyblish.plugin.Config()

# Setup
HOST = 'python'
FAMILY = 'test.family'

REGISTERED = pyblish.plugin.registered_paths()
PACKAGEPATH = pyblish.lib.main_package_path()
ENVIRONMENT = os.environ.get("PYBLISHPLUGINPATH", "")
PLUGINPATH = os.path.join(PACKAGEPATH, '..', 'tests', 'plugins')


def setup():
    """Disable default plugins and only use test plugins"""
    config = pyblish.plugin.Config()
    config['paths'] = []

    pyblish.plugin.deregister_all_paths()


def setup_empty():
    """Disable all plug-ins"""
    setup()
    pyblish.plugin.deregister_all_paths()
    pyblish.plugin.deregister_all_hosts()
    pyblish.plugin.deregister_all_callbacks()


def teardown():
    """Restore previously REGISTERED paths"""

    # Clear singletons
    pyblish.plugin.Config._instance = None

    pyblish.plugin.deregister_all_paths()
    for path in REGISTERED:
        pyblish.plugin.register_plugin_path(path)

    os.environ["PYBLISHPLUGINPATH"] = ENVIRONMENT
    pyblish.api.deregister_all_plugins()
    pyblish.api.deregister_all_hosts()
    pyblish.api.deregister_test()
    pyblish.api.__init__()


@contextlib.contextmanager
def captured_stdout():
    """Temporarily reassign stdout to a local variable"""
    try:
        sys.stdout = StringIO()
        yield sys.stdout
    finally:
        sys.stdout = sys.__stdout__


@contextlib.contextmanager
def captured_stderr():
    """Temporarily reassign stderr to a local variable"""
    try:
        sys.stderr = StringIO()
        yield sys.stderr
    finally:
        sys.stderr = sys.__stderr__


@contextlib.contextmanager
def tempdir():
    """Provide path to temporary directory"""
    try:
        tempdir = tempfile.mkdtemp()
        yield tempdir
    finally:
        shutil.rmtree(tempdir)
