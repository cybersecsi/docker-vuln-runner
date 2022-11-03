import json
import os
from docker_vuln_runner.vuln import vuln_home
from docker_vuln_runner.helper import *

"""Manage the hosts file
"""

HOSTS_FILE = "hosts.json"


def hosts_file():
    return os.path.join(vuln_home(), HOSTS_FILE)

def hosts_exists():
    return os.path.exists(hosts_file())


def hosts_init(token):
        h = Hosts(token)
        with open(hosts_file(), 'w') as f:
                f.write(h.to_json())

def hosts_read():
    with open(hosts_file(), 'r') as f:
        file_content = f.read()
        try:
            json_content = json.loads(file_content)
            token = json_content['token']
            envs = json_content['envs']
            h = Hosts(token, envs)
            return h

        except FileNotFoundError:
            json_content = None
        except json.decoder.JSONDecodeError:
        # Cannot read the file
            json_content = None

def token_initialized():
    try : 
        h = hosts_read()
        return h
    except Exception: 
        return False

class Hosts:
    def __init__(self, token, envs = {}):
        self.token = token
        self.envs = envs

    def add_host(self, host):
        self.envs[host] = []

    def to_json(self):
        return json.dumps(self.__dict__, indent = 2)
    
    def update(self):
        with open(hosts_file(), 'w') as f:
                f.write(self.to_json())
