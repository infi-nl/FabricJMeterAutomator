=== Fabric JMeter load test automator ===

-- Introduction --

This Fabric script can be used to automatically install and run a JMeter load test on multiple server instances
without having to manually configure each instance. The server instances are required to be accessible through
SSH using key-file authentication, and should also allow JMeter communication between eachother (meaning, firewall
settings etc. should be properly configured). Furthermore, a working Java installation is necessary on each server
in order to run JMeter.

The script has been tested on Amazon EC2 Ubuntu servers, but is expected to be compatible with similar set-ups
as well. Please share your own experiences!

-- HOWTO --

1. Install Fabric

	- Install python 2.7 (https://www.python.org/ftp/python/2.7.6/python-2.7.6.amd64.msi)
		- If necessary, add python.exe to the PATH environment variable
	- Install PyCrypto 2.6 (http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py2.7.exe)
	- Install pip:
		- Download https://raw.github.com/pypa/pip/master/contrib/get-pip.py
		- Open a command prompt in the folder where the file has been downloaded
		- Execute: 
			python get-pip.py
		- If necessary, add pip.exe to the PATH environment variable
	- Install fabric:
		- pip install fabric	

2. Create JMeter installation zip file

	You will need a working installation of JMeter to be used for the load test. Create a zip archive
	named 'jmeter.zip' with the installation in the archive root. Place this file in the same directory
	as fabfile.py.

3. Create loadtest zip file

	A JMeter JMX file (named loadtest.jmx) specifying the script for the load test is also required. 
	To allow control over the amount of threads and loops used in the load test, specify these values
	in your JMX script as ${__P(users)} (for thread count) and ${__P(count)} (for loop count).

	Create a zip archive named 'loadtest.zip' containing the loadtest.jmx file and any additional
	data files (if referenced from within the JMX script). Place this file in the same directory
	as fabfile.py.

4. Gather authentication key-file

	Furthermore, to authenticate on the remote servers, a key-file is required. Note the local path
	of this key-file, or place it in the same folder as fabfile.py. Specify the full path in the 
	configuration file (see Step 5).	

5. Adjust configuration

	Edit config.py and properly set the config values. A brief explanation of each config setting can
	be read below:

	- ssh_key_file:		Full path to key-file that is used to authenticate at the remote servers
						(NOTE: currently only key-file authentication is supported by this Fabric script)

	- ssh_user: 		Username to be used to authenticate at remote servers

    - remote_base_path: Remote path in which JMeter will be installed. Within this path a new folder
    				    will be created for each session identifier you use.

    - control_host: 	Server IP which will be used to run the load test

    - remote_hosts: 	Additional list of server IPs which are used as additional JMeter server instances,
    					separated by ';' (eg. '1.1.1.1;2.2.2.2;3.3.3.3')

6. Install JMeter and load test on remote servers

	- In the directory where fabfile.py (and jmeter.zip and loadtest.zip) reside, run:

		fab install:<identifier>

	  Where <identifier> is a string value that allows you to give a unique name to the load test session.
      Example:

		fab install:jmeter_firsttest

	  NOTE: If you already installed JMeter with the given session identifier you will have to use the
	       'reinstall' command to confirm you want to overwrite the existing installation.
	       Example:

	       	   fab reinstall:jmeter_firsttest

	- If you make changes to the JMX script, you can use the 'reinstall_loadtest' command to update
	  the script on the remote hosts.

	  Example:

	  	fab reinstall_loadtest:jmeter_firsttest

	  Also, the same command exists for the JMeter installation:

	  	fab reinstall_jmeter:jmeter_firsttest

7. Run JMeter load test

	To start the load test the following command can be used:

		fab start:<identifier>,<threads>,<loops>

	Where the <identifier> is again the session identifier used, which should be the same as the identifier
	used when installing JMeter and the load test script earlier. The <threads> and <loops> parameters 
	specify the amount of threads and loops that will be used during the load test (note that for this to
	work the JMX file should use these parameterized values, as described in Step 3).

	Example:

		fab start:jmeter_firsttest,10,10

	The above command will use your installation of 'jmeter_firsttest', and will run the load test with
	10 threads and in 10 loops.

-- Troubleshooting --

Mail me: jiri.bakker@infi.nl

