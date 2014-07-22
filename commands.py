from __future__ import with_statement
from fabric.api import *
from fabric.contrib.files import exists
import time

timestamp = time.strftime('%Y%m%d%H%M%S')

# Install JMeter on host
# Expects local file 'jmeter.zip' containing a JMeter installation to be used for the loadtest. The installation should be placed in the archive root.
def execute_install_jmeter(identifier, path, force): 
    if force:
        run('rm -rf ' + path) # TODO potentieel gevaarlijk! Safety inbouwen

    if exists(path):
        raise Exception('A JMeter installation already exists for session identifier \'' + identifier + '\'. Please remove this installation, or force installation (fab reinstall:<identifier>)')

    run("mkdir -p %s" % path)

    upload_and_unzip('jmeter.zip', path, force)        

    with cd(path):        
        run('chmod +x bin/jmeter')
        run('chmod +x bin/jmeter-server')

    if not exists(path + '/bin/jmeter'):
        raise Exception('No JMeter binary found in output directory. Ensure jmeter.zip contains a valid JMeter installation (including a \'bin\' folder) in the root of the archive.')

# Install loadtest script on host
# Expects local file 'loadtest.zip' containing at least a 'loadtest.jmx' file in the root specifying the JMeter test. Any additional files (eg. .csv) should also be placed in the archive root.
def execute_install_loadtest(identifier, path, force):    
    if force:
        run('rm -f ' + path + '/bin/loadtest.jmx') # TODO potentieel gevaarlijk! Safety inbouwen

    if exists(path + '/bin/loadtest.jmx'):
        raise Exception('A loadtest.jmx file already exists for session identifier \'' + identifier + '\'. Please remove this file, or force installation (fab reinstall:<identifier>)')

    upload_and_unzip('loadtest.zip', path + '/bin', force)

    if not exists(path + '/bin/loadtest.jmx'):
        raise Exception('loadtest.jmx not found in output directory. JMeter loadtest cannot be run without this file. Ensure loadtest.zip contains this file in the root of the archive.')
            
# Start JMeter server daemon (in background screen session to ensure it does not end when SSH session is disconnected)
def start_jmeter_server(identifier, path):    
    with cd(path + '/bin'):
        run('screen -d -m -S jmeter-session-' + identifier + ' ./jmeter-server -n -X', pty=False)

# Start load test from control host, using all hosts
def start_jmeter_loadtest(path, allHosts, threads, loops):
    with cd(path + '/bin'):
        run('./jmeter -n -t loadtest.jmx -R ' + ','.join(allHosts) + ' -l ' + timestamp + '.jtl -Gusers=' + threads + ' -Gcount=' + loops)

# Ensure screen sessions are closed 
def close_screen_sessions(identifier):
    run('screen -ls | grep ' + identifier + ' | cut -d. -f1 | awk \'{print $1}\' | xargs kill')

# Download JMeter logfile
def get_jmeter_logs(identifier):
    get('~/jmeter/' + identifier + '/bin/' + timestamp + '.jtl', 'jmeterlog_' + timestamp + '.jtl')    


# Upload zip file, unpack contents and clean up
def upload_and_unzip(filename, path, force=False):
    with cd(path):
        # Upload file
        put(filename, path)

        # Ensure 'unzip' is installed
        run('sudo apt-get -qqq install unzip')

        # Unzip file contents to bin directory (needed to ensure jmx script can be executed with correct working directory)
        if force:
            run('unzip -qq -o ' + filename)
        else:
            run('unzip -qq ' + filename)

        # Clean up zip file
        run('rm ' + filename)