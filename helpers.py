from fabric.api import run, env
from config import get_config_value
import re

# Initialize environment
def init_ssh():
	env.user =  get_config_value('ssh_user')
	env.key_filename = [get_config_value('ssh_key_file')]

# Build path for given identifier
def get_path(identifier):
	if not is_valid_identifier(identifier):
		raise Exception('Session identifier \'' + identifier + '\' is not in a valid format. Session identifier can only contain alphanumerical characters or on of the following special characters: _ - .')
	return get_config_value('remote_base_path') + '/' + identifier

# Validate session identifier (alphanumerical and one of these characters: _ - .)
def is_valid_identifier(identifier):
	pattern = re.compile(r"^([a-zA-z0-9_\.\-]{0,255})$", re.VERBOSE | re.IGNORECASE)
	return pattern.match(identifier) is not None

# Convert string of IP address separated by ';' to a list while validating each IP address
def get_hosts_array_from_string(hostsString):
	if isinstance(hostsString, str):
		hostsArray = hostsString.split(';')
		for host in hostsArray:
			if not is_valid_ipv4(host):
				raise Exception('\'' + host + '\' is not a valid IP address')
		return hostsArray

# Combine 'remote_hosts' with 'control_host' config values to retrieve a list of all hosts to be used
def get_all_hosts():
	hostsArray = get_hosts_array_from_string(get_config_value('remote_hosts'))
	hostsArray.append(get_config_value('control_host'))
	return hostsArray  


# Source: http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
def is_valid_ipv4(ip):
	pattern = re.compile(r"""
		^
		(?:
		  # Dotted variants:
		  (?:
			# Decimal 1-255 (no leading 0's)
			[3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
		  |
			0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
		  |
			0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
		  )
		  (?:                  # Repeat 0-3 times, separated by a dot
			\.
			(?:
			  [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
			|
			  0x0*[0-9a-f]{1,2}
			|
			  0+[1-3]?[0-7]{0,2}
			)
		  ){0,3}
		|
		  0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
		|
		  0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
		|
		  # Decimal notation, 1-4294967295:
		  429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
		  42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
		  4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
		)
		$
	""", re.VERBOSE | re.IGNORECASE)
	return pattern.match(ip) is not None