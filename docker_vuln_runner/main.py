import docker_vuln_runner.helper as helper
from docker_vuln_runner.vuln import Vuln, Vulnenv, vuln_home, get_vuln_objects, all_ports, get_duplicates, vuln_init, check_init, vuln_update, is_initialized, vuln_names, run_vuln, find_vuln_projects, down_vuln, check_docker
import typer
import json
import os


typer_app = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]})


@typer_app.command()
def init():
    """"
    Initialize vuln-runner    
    """
    helper.banner()
    check_docker()
    if is_initialized():
        helper.bold("vulhub already initialized!")
    else:
        helper.log("Init vuln-runner")
        vuln_init()
        helper.success("Vuln initialized!")


@typer_app.command()
def list(silent: bool = typer.Option(False, "--silent", "-s")):
    """
    List the vulhub cves
    """
    helper.banner(silent)
    check_init()
    helper.log("Find vuln repo in {}".format(vuln_home()), silent)
    vulhubs = find_vuln_projects(vuln_home())
    names = vuln_names(vulhubs)
    print("\n".join(names))


@typer_app.command()
def update():
    """
    Update the vulhub git repository
    """
    helper.banner()
    check_init()
    vuln_update()
    helper.success("Vuln updated!")


@typer_app.command()
def run(vulhub_names: str, silent: bool = typer.Option(False, "--silent")):
    """
    Run a list of vuln projects

    Args:
        vulhub_names (str): A comma-separated list of vuln projects
        silent (bool, optional): Silent mode, disable the log to parse the output. Defaults to False
    """
    helper.banner(silent)
    check_init()
    helper.log("Find vuln repos in {}".format(vuln_home()), silent)
    vulhubs = find_vuln_projects(vuln_home())
    vulhub_names = vulhub_names.split(",")
    vulhub_objects = get_vuln_objects(vulhubs, vulhub_names)
    ports = all_ports(vulhub_objects)
    duplicates = get_duplicates(ports)
    if len(duplicates) > 0:
        helper.err(
            "Cannot run, the following ports are duplicates: {}".format(duplicates))

    # Ok, now run
    for vn in vulhub_names:
        helper.log("Run {}".format(vn))
        run_vuln(vulhubs, vn)


@typer_app.command()
def down(vulhub_names: str, silent: bool = typer.Option(False, "--silent")):
    """
    Down a list of vuln projects

    Args:
        vulhub_names (str): A comma-separated list of vuln projects
        silent (bool, optional): Silent mode, disable the log to parse the output. Defaults to False
    """

    helper.banner(silent)
    check_init()
    helper.log("Find vuln repo in {}".format(vuln_home()), silent)
    vulhubs = find_vuln_projects(vuln_home())
    vulhub_names = vulhub_names.split(",")
    vulhub_objects = get_vuln_objects(vulhubs, vulhub_names)
    for vn in vulhub_objects:
        vn.down()


@typer_app.command()
def generate_vulnenv(no_vulns: int, no_env: int = 1):
    """
    Generate <no_env> vulnerable environments composed of <no_vulns> stacks
        Each environment has no port conflicts. It is useful to run different vulhub projects on different machines.
    Args:
        no_vulns (int): The number of vulnerable compose
        no_env (int, optional): The number of vulnerable environments. Defaults to 1.
    """
    helper.banner(True)
    check_init()
    vulhubs = find_vuln_projects(vuln_home())
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
    check_init()
    vulhubs = find_vuln_projects(vuln_home())
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
                    run_vuln(vulhubs, v['name'])

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
    check_init()
    vulhubs = find_vuln_projects(vuln_home())
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
                    down_vuln(vulhubs, v['name'])

            except Exception as e:
                # Cannot read the file
                helper.err("Invalid environment json file")
    else:
        helper.err("Please give me a valid file")

def app():
    typer_app()
