from yaml import safe_load, load, SafeLoader, dump
from pathlib import Path
from docker_vuln_runner.helper import log, err, get_compose_name
import os
import glob
from git import Repo
import git
import json
from python_on_whales import DockerClient, docker as docker_cli


class VulnRepo:
    """A vulnerable repository instance
    """
    def __init__(self, name, repo):
        self.name = name
        self.repo = repo

    def home(self):
        return os.path.join(vuln_home(), self.name)

VULN_REPOS = [
    VulnRepo("vulhub", "https://github.com/vulhub/vulhub")
]


def get_duplicates(ports):
    newlist = [] # empty list to hold unique elements from the list
    duplist = [] # empty list to hold the duplicate elements from the list
    for i in ports:
        if i not in newlist:
            newlist.append(i)
        else:
            duplist.append(i) # this method catches the first duplicate entries, and appends them to the list
    return duplist



def all_ports(vulns):
    """Returns a list of ports from a list of objects

    Args:
        vulns (list): A list of objects

    Returns:
        list: the list of ports
    """
    ports = []
    for v in vulns:
        ports.extend(v.ports())
    return ports

def vuln_contains(vulns, name):
    """Return true when the vuln is present in the list of vulns

    Args:
        vulns (list): The list of vulns
        name (str): The vuln name

    Returns:
        bool: True when
    """
    for v in vulns:
        if v.equal(name):
            return True
    return False


def find_by_name(vulns, name):
    """Find the

    Args:
        vulns (list<Vuln>): The list of vuln objects
        name (str): The vuln name

    Raises:
        Exception: when the vuln is not found

    Returns:
        Vuln: The found vuln object
    """
    found = [v for v in vulns if v.name == name]
    if not found:
        raise Exception("{} not found".format(name))

    return found[0]

def paths(vulns):
    return [v.path for v in vulns]

def vuln_names(vulns):
    return [v.name for v in vulns]



def find_repo_projects(base_name, base_path, virtual = False):
    ret = []
    for filename in glob.iglob(os.path.join(base_path, '**/docker-compose.yml'), recursive=True):
        if virtual:
            filename = filename.replace(vuln_home(), virtual_vuln_home())
        ret.append(Vuln("{}.{}".format(base_name, get_compose_name(filename)), filename))
    return ret

def find_vuln_projects(base_path, virtual = False):
    ret = []
    for V in VULN_REPOS:
        ret = ret + find_repo_projects(V.name, base_path, virtual)

    return ret

def run_vuln(vulns, vuln_name):
    if not vuln_contains(vulns, vuln_name):
        err("{} vuln not found".format(vuln_name))

    vuln_obj = find_by_name(vulns, vuln_name)
    vuln_obj.run()


def down_vuln(vulns, vuln_name):
    if not vuln_contains(vulns, vuln_name):
        err("{} vuln not found".format(vuln_name))

    vuln_obj = find_by_name(vulns, vuln_name)
    vuln_obj.down()

def get_ports(vulns, vuln_name):
    if not vuln_contains(vulns, vuln_name):
        err("{} vuln not found".format(vuln_name))
    vuln_obj = find_by_name(vulns, vuln_name)
    return vuln_obj.ports()

def get_vuln_objects(vulns, names):
    return [v for v in vulns if v.name in names]

def vuln_home():
    """
        Returns the base vuln home
    """
    home_folder = Path.home()
    config_folder = os.path.join(home_folder, '.vulnenv')
    return config_folder

def virtual_vuln_home():
    return "{}".format("VULN_HOME")

def vuln_init():
    if not os.path.isdir(vuln_home()):
        os.mkdir(vuln_home())
    for v in VULN_REPOS:
        log("Clone {} in {}".format(v.repo, v.home()))
        Repo.clone_from(v.repo, v.home())

def check_docker():
    if not docker_cli.compose.is_installed():
        err("""
        Please install 'docker compose' (version 2)

        ```
        sudo systemctl stop docker
        sudo systemctl stop docker.socket
        sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-compose-plugin
        curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
        sudo bash /tmp/get-docker.sh
        ```

        """)
def check_init():
    check_docker()
    if not is_initialized():
        err("{} does not exist, please run \"vuln-runner init\" first".format(vuln_home()))


def vuln_update():
    for V in VULN_REPOS:
        log("Update {} repo in {}".format(V.repo, V.home()))
        g = git.cmd.Git(V.home())
        g.pull()


def is_initialized():
    return os.path.exists(vuln_home()) and len(os.listdir(vuln_home())) != 0




    # def name(self, vulnerable_name):
    #     return "{}.{}".format(self.name, vulnerable_name)

class Vuln:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.compose = None

    def equal(self, name):
        """Returns true when the compose name is equal to the vuln name

        Args:
            name (str): The vuln name

        Returns:
            bool: True when the vuln is equal
        """
        return self.name == name

    def load_compose(self):
        """Load the docker-compose object
        """
        real_path = self.path.replace("VULN_HOME", vuln_home())
        if self.compose is None:
            with open(real_path) as stream:
                self.compose = safe_load(stream)

    def down(self):
        docker = DockerClient(compose_files=[self.path])
        docker.compose.down()

    def run(self):
        docker = DockerClient(compose_files=[self.path])
        docker.compose.up(detach=True)

    def ports(self):
        """Returns the list of ports

        Returns:
            list<port>: The list of ports
        """
        self.load_compose()
        list_ports = []
        for s, value in self.compose['services'].items():
            if 'ports' in value:
                ports = value['ports']
                # Replace the ports with the new port
                for p in ports:
                    splitted = p.split(":")
                    binded = int(splitted[0])
                    second = splitted[1]
                    # If the new port was found
                    list_ports.append(binded)
        return list_ports




    def to_obj(self):
        """Returns a json representation of a vuln

        Returns:
            json: A json representation of the vuln object
        """
        return {
            "name" : self.name,
            "path" : self.path,
            "ports" : self.ports()
        }




class Vulnenv:
    def __init__(self, vulns):
        self.envs = {}
        self.vulns = vulns

    def add_env(self,  env_id, vulns):
        """Add a new enviornment

        Args:
            vulh_obj (Vuln): A Vuln object
        """
        self.envs[env_id] = [v.to_obj() for v in vulns]

    def create_env(self, env_id, no_vulns, virtual = False):
        """Collect the list of vulnerabilities,
        create an env and add to the internal structure

        Args:
            env_id (_type_): _description_
            no_vulns (_type_): _description_
            all_vulns (_type_): _description_
        """
        collected_vulns = []
        busy_ports = []
        no_collected = 0
        for v in self.vulns:
            new_ports = v.ports()
            test_ports = busy_ports + new_ports
            if not get_duplicates(test_ports):
                busy_ports.extend(v.ports())
                no_collected = no_collected + 1
                collected_vulns.append(v)
                self.vulns.remove(v)
            if no_collected == no_vulns:
                break
        if len(collected_vulns) == 0:
            raise Exception("Not available envs. Try with lesser environments or ports")
        self.add_env(env_id, collected_vulns)


    def to_json(self):
        return json.dumps({
            "envs":  self.envs
        }, indent = 2)
