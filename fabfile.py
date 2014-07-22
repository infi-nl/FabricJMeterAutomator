from fabric.tasks import execute
from config import get_config_value
from helpers import *
from commands import *

# Install
def install(identifier):
    init_ssh()
    path = get_path(identifier)
    allHosts = get_all_hosts()

    execute(execute_install_jmeter,   identifier=identifier, path=path, force=False, hosts=allHosts)
    execute(execute_install_loadtest, identifier=identifier, path=path, force=False, hosts=allHosts)

def install_jmeter(identifier):
    init_ssh()
    path = get_path(identifier)

    execute(execute_install_jmeter,   identifier=identifier, path=path, force=False, hosts=get_all_hosts())

def install_loadtest(identifier):
    init_ssh()
    path = get_path(identifier)

    execute(execute_install_loadtest, identifier=identifier, path=path, force=False, hosts=get_all_hosts())

# Reinstall (delete existing files)
def reinstall(identifier):
    init_ssh()
    path = get_path(identifier)
    allHosts = get_all_hosts()

    execute(execute_install_jmeter,   identifier=identifier, path=path, force=True, hosts=allHosts)
    execute(execute_install_loadtest, identifier=identifier, path=path, force=True, hosts=allHosts)

def reinstall_jmeter(identifier):
    init_ssh()
    path = get_path(identifier);

    execute(execute_install_jmeter,   identifier=identifier, path=path, force=True, hosts=get_all_hosts())

def reinstall_loadtest(identifier):
    init_ssh()
    path = get_path(identifier)

    execute(execute_install_loadtest, identifier=identifier, path=path, force=True, hosts=get_all_hosts())

# Start loadtest
def start(identifier, threads, loops):
    init_ssh()
    path = get_path(identifier)
    controlHost = get_config_value('control_host')
    allHosts    = get_all_hosts()

    execute(start_jmeter_server,   identifier=identifier, path=path, hosts=allHosts)
    execute(start_jmeter_loadtest, path=path, allHosts=allHosts, threads=threads, loops=loops, hosts=controlHost)
    execute(close_screen_sessions, identifier=identifier, hosts=allHosts)
    execute(get_jmeter_logs,       identifier=identifier, hosts=controlHost)