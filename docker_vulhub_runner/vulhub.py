from yaml import safe_load, load, SafeLoader, dump
from pathlib import Path
import os
from git import Repo
import git 
import json


from python_on_whales import DockerClient


class Vulhub:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.compose = None

    def equal(self, name):
        """Returns true when the compose name is equal to the vulhub name

        Args:
            name (str): The vulhub name

        Returns:
            bool: True when the vulhub is equal
        """
        return self.name == name

    def load_compose(self):
        """Load the docker-compose object
        """
        if self.compose is None:
            with open(self.path) as stream:
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


    def paths(vulhubs):
        return [v.path for v in vulhubs]

    def names(vulhubs):
        return [v.name for v in vulhubs]

    def contains(vulhubs, name):
        """Return true when the vulhub is present in the list of vulhubs

        Args:
            vulhubs (list): The list of vulhubs
            name (str): The vulhub name

        Returns:
            bool: True when 
        """
        for v in vulhubs:
            if v.equal(name):
                return True
        return False

    def find_by_name(vulhubs, name):
        """Find the 

        Args:
            vulhubs (list<Vulhub>): The list of vulhub objects
            name (str): The vulhub name

        Raises:
            Exception: when the vulhub is not found

        Returns:
            Vulhub: The found vulhub object
        """
        found = [v for v in vulhubs if v.name == name]
        if not found:
            raise Exception("{} not found".format(name))

        return found[0]

    def to_obj(self):
        """Returns a json representation of a vulhub

        Returns:
            json: A json representation of the vulhub object
        """
        return {
            "name" : self.name,
            "path" : self.path,
            "ports" : self.ports()
        }     

    def get_vulhub_objects(vulhubs, names):
        return [v for v in vulhubs if v.name in names]

    def get_duplicates(ports):
        newlist = [] # empty list to hold unique elements from the list
        duplist = [] # empty list to hold the duplicate elements from the list
        for i in ports:
            if i not in newlist:
                newlist.append(i)
            else:
                duplist.append(i) # this method catches the first duplicate entries, and appends them to the list
        return duplist



    def all_ports(vulhubs):
        """Returns a list of ports from a list of objects

        Args:
            vulhubs (list): A list of objects

        Returns:
            list: the list of ports
        """
        ports = []
        for v in vulhubs:
            ports.extend(v.ports())
        return ports

    def home():
        home_folder = Path.home()
        config_folder = os.path.join(home_folder,'.vulhub')
        return config_folder

    def init():
        Repo.clone_from("https://github.com/vulhub/vulhub.git", Vulhub.home())

    def update():
        g = git.cmd.Git(Vulhub.home())
        g.pull()


    def is_initialized():
        return os.path.exists(Vulhub.home())



class Vulnenv:
    def __init__(self, vulhubs):
        self.envs = {}
        self.vulhubs = vulhubs

    def add_env(self,  env_id, vulhubs):
        """Add a new enviornment

        Args:
            vulh_obj (Vulnhub): A vulnhub object
        """
        self.envs[env_id] = [v.to_obj() for v in vulhubs]

    def create_env(self, env_id, no_vulns):
        """Collect the list of vulnerabilities, 
        create an env and add to the internal structure

        Args:
            env_id (_type_): _description_
            no_vulns (_type_): _description_
            all_vulhubs (_type_): _description_
        """
        collected_vulns = []
        busy_ports = []
        no_collected = 0
        for v in self.vulhubs:
            new_ports = v.ports()
            test_ports = busy_ports + new_ports 
            if not Vulhub.get_duplicates(test_ports):
                busy_ports.extend(v.ports())
                no_collected = no_collected + 1
                collected_vulns.append(v)
                self.vulhubs.remove(v)
            if no_collected == no_vulns:
                break
        if len(collected_vulns) == 0:
            raise Exception("Not available envs. Try with lesser environments or ports")
        self.add_env(env_id, collected_vulns)

    def to_json(self):
        return json.dumps({
            "envs":  self.envs
        }, indent = 2)