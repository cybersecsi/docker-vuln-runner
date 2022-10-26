import docker_vulhub_runner.helper as helper
from docker_vulhub_runner.vulhub import Vulhub, Vulnenv
import typer
import json
import os


typer_app = typer.Typer(add_completion=False)


@typer_app.command()
def init():
    helper.banner()
    if Vulhub.is_initialized():
        helper.bold("vulhub already initialized!")
    else:
        helper.log("Clone vulhub in {}".format(Vulhub.home()))
        Vulhub.init()
        helper.success("Vulhub initialized!")


@typer_app.command()
def list(silent: bool = typer.Option(False, "--silent")):
    """
    List the vulhub cves
    """
    helper.banner(silent)
    helper.check_init()
    helper.log("Find vulhub repo in {}".format(Vulhub.home()), silent)
    vulhubs = helper.find_vulhub_projects(Vulhub.home())
    names = Vulhub.names(vulhubs)
    print("\n".join(names))


@typer_app.command()
def update():
    """Update the vulhub git repository
    """
    helper.banner()
    helper.check_init()
    Vulhub.update()
    helper.success("Vulhub updated!")


@typer_app.command()
def run(vulhub_names: str, silent: bool = typer.Option(False, "--silent")):
    """Run a list of vulhub projects

    Args:
        vulhub_names (str): A comma-separated list of vulhub projects
        silent (bool, optional): Silent mode, disable the log to parse the output. Defaults to False
    """
    helper.banner(silent)
    helper.check_init()
    helper.log("Find vulhub repo in {}".format(Vulhub.home()), silent)
    vulhubs = helper.find_vulhub_projects(Vulhub.home())
    vulhub_names = vulhub_names.split(",")
    vulhub_objects = Vulhub.get_vulhub_objects(vulhubs, vulhub_names)
    ports = Vulhub.all_ports(vulhub_objects)
    duplicates = Vulhub.get_duplicates(ports)
    if len(duplicates) > 0:
        helper.err(
            "Cannot run, the following ports are duplicates: {}".format(duplicates))

    # Ok, now run
    for vn in vulhub_names:
        helper.log("Run {}".format(vn))
        helper.run_vulhub(vulhubs, vn)


@typer_app.command()
def down(vulhub_names: str, silent: bool = typer.Option(False, "--silent")):
    """Down a list of vulhub projects

    Args:
        vulhub_names (str): A comma-separated list of vulhub projects
        silent (bool, optional): Silent mode, disable the log to parse the output. Defaults to False
    """

    helper.banner(silent)
    helper.check_init()
    helper.log("Find vulhub repo in {}".format(Vulhub.home()), silent)
    vulhubs = helper.find_vulhub_projects(Vulhub.home())
    vulhub_names = vulhub_names.split(",")
    vulhub_objects = Vulhub.get_vulhub_objects(vulhubs, vulhub_names)
    for vn in vulhub_objects:
        vn.down()


@typer_app.command()
def generate_vulnenv(no_vulns: int, no_env: int = 1):
    """Generate <no_env> vulnerable environments composed of <no_vulns> stacks
        Each environment has no port conflicts. It is useful to run different vulhub projects on different machines.
    Args:
        no_vulns (int): The number of vulnerable compose
        no_env (int, optional): The number of vulnerable environments. Defaults to 1.
    """
    helper.banner(True)
    helper.check_init()
    vulhubs = helper.find_vulhub_projects(Vulhub.home())
    vuln_env = Vulnenv(vulhubs)

    try:
        for i in range(0, no_env):
            vuln_env.create_env(i, no_vulns)

    except Exception as e:
        helper.err(e)
    print(vuln_env.to_json())


@typer_app.command()
def run_env(json_file: str, id_env: int):
    """Run an environment taken from a JSON configuration file

    Args:
        json_file (str): The path of the json file
        id_env (int): The environment ID
    """
    helper.banner(True)
    helper.check_init()
    vulhubs = helper.find_vulhub_projects(Vulhub.home())
    if os.path.isfile(json_file):
        with open(json_file) as myfile:
            file_content = myfile.read()
            try:
                json_content = json.loads(file_content)
                envs = json_content['envs']
                if str(id_env) not in envs.keys():
                    helper.err("No valid id_env: {}".format(id_env))
                vuln_list = envs[str(id_env)]
                for v in vuln_list:
                    helper.run_vulhub(vulhubs, v['name'])

            except Exception as e:
                # Cannot read the file
                helper.err("Invalid environment json file")
    else:
        helper.err("Please give me a valid file")

@typer_app.command()
def down_env(json_file: str, id_env: int):
    """Down an environment

    Args:
        json_file (str): The path of the json file
        id_env (int): The environment ID
    """

    helper.banner(True)
    helper.check_init()
    vulhubs = helper.find_vulhub_projects(Vulhub.home())
    if os.path.isfile(json_file):
        with open(json_file) as myfile:
            file_content = myfile.read()
            try:
                json_content = json.loads(file_content)
                envs = json_content['envs']
                if str(id_env) not in envs.keys():
                    helper.err("No valid id_env: {}".format(id_env))
                vuln_list = envs[str(id_env)]
                for v in vuln_list:
                    helper.down_vulhub(vulhubs, v['name'])

            except Exception as e:
                # Cannot read the file
                helper.err("Invalid environment json file")
    else:
        helper.err("Please give me a valid file")

def app():
    typer_app()
