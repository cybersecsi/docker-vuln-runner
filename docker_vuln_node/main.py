import typer
from docker_vuln_controller.main import check_initialization
from docker_vuln_runner.vuln import is_initialized, vuln_home
from docker_vuln_runner.helper import err, log, check_network
from docker_vuln_runner.hosts import *
from docker_vuln_node.node import * 

typer_app = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]})

def app():
    typer_app()


@typer_app.command()
def init():
    # token: str=  typer.Option(..., prompt="Setup the token", confirmation_prompt=False, hide_input=True, callback=init_callback)):
    init_confirm = True
    if hosts_exists():
        init_confirm = typer.confirm("hosts already present, are you sure to init?")
    if init_confirm:
        token = typer.prompt("Setup the token", hide_input = True)
        hosts_init(token)
        log("hosts.json created!")


@typer_app.callback()
def check_initialization():
    if not is_initialized():
        err("{} does not exist, please run \"vuln-runner init\" first".format(vuln_home()))

def check_token():
    h = token_initialized()
    if not h:
        err("Token not initialized, please run \"vuln-node init\" first")
    return h



# Start the vuln-node
@typer_app.command()
def start():
    check_initialization()
    h = check_token()
    VulnNode(h)
