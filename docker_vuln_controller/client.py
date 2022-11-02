import socket
import sys
import json
from docker_vuln_runner.helper import err, log, warn, VERSION

NODE_PORT = 4545
TIMEOUT_SOCKET = 0.0001

def _msg(token, type, data = None):
    if data: 
        return json.dumps({
            "token":  token, 
            "msg": type, 
            "data": data
        })

    else: 
        return json.dumps({
            "token":  token, 
            "msg": type, 
        })

def hello(token):
    return _msg(token, "hello")

def run(token, cves):
    return _msg(token, "run", cves)

def parse_version(version_string):
    v_number = version_string.split()[1].replace('v', '')
    return v_number

class VulnClient:
    def __init__(self, ip, token):
        try:
            self.sock = socket.socket()
            self.sock.settimeout(TIMEOUT_SOCKET)
            self.token = token

        except socket.error as err:
            err('Socket error because of %s' % (err))
        self.address = ip

    def ping(self):
        ret = False
        try:
            self.sock.connect((self.address, NODE_PORT))
            self.sock.send(hello(self.token).encode('utf-8'))
            # Receive
            version_string = self.sock.recv(1024).decode()
            version_number = parse_version(version_string)
            if version_number == VERSION:
                ret = True
            else: 
                warn("vuln-node found but different version. Controller version: {}, node version:{}".format(VERSION, version_number))
            

        except socket.gaierror:
                err('There an error resolving the host')

        except socket.timeout:
            pass
        except Exception as e:
            warn("Error in version detection")

        self.sock.close()
        return ret

    def run(self, cves):
        ret = False
        try:
            self.sock.connect((self.address, NODE_PORT))
            self.sock.send(run(self.token, cves).encode('utf-8'))
            # Receive
            ret = self.sock.recv(1024).decode()
            

        except socket.gaierror:
                err('There an error resolving the host')

        except Exception as e:
            err("Communication error: {}".format(e))

        self.sock.close()
        return ret
        
