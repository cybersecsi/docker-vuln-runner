import socket
from docker_vuln_runner.helper import err, log, VERSION
from docker_vuln_runner.vuln import Vuln, Vulnenv, vuln_home, get_vuln_objects, all_ports, get_duplicates, vuln_init, check_init, vuln_update, is_initialized, vuln_names, run_vuln, find_vuln_projects, down_vuln, check_docker
from docker_vuln_runner.message import VulnMessage

NODE_PORT = 4545
 

class VulnNode:
    def __init__(self, hosts_obj):
        self.sock = socket.socket()
        self.sock.bind(('0.0.0.0', NODE_PORT))
        self.sock.listen(5)
        self.vulhubs = find_vuln_projects(vuln_home())
        self.hosts_obj = hosts_obj
        log("vuln-node v{} started".format(VERSION))
        while True:
            c, addr = self.sock.accept()
            log('got connection from {}'.format(addr))

            jsonReceived = c.recv(1024)

            # log("Json received --> {}".format(jsonReceived))
            vuln_message = VulnMessage.parse_json(jsonReceived)
            if vuln_message.is_hello():
                c.send("vuln-runner v{}".format(VERSION).encode('utf-8'))

            elif vuln_message.is_run():
                vuln_envs = vuln_message.data
                for v in vuln_envs:
                    run_vuln(self.vulhubs, v['name'])


            c.close()

    def shutdown(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

