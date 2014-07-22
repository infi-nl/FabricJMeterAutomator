config = {
    'ssh_key_file': '',
    'ssh_user': '',
    'remote_base_path': '',
    'control_host': '',
    'remote_hosts': ''
}

def get_config_value(key):
    return config[key]