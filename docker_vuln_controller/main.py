import typer
from docker_vuln_runner.vuln import Vulnenv, is_initialized, vuln_home, find_vuln_projects, virtual_vuln_home
from docker_vuln_runner.helper import err, log, success, check_network
from docker_vuln_runner.hosts import *
from docker_vuln_controller.client import *

import json


def init_callback(v): 
    print("Version: {}".format(v))

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

    pass


@typer_app.callback()
def check_initialization():
    if not is_initialized():
        err("{} does not exist, please run \"vuln-runner init\" first".format(vuln_home()))

def check_token():
    h = token_initialized()
    if not h:
        err("Token not initialized, please run \"vuln-controller init\" first")
    return h

@typer_app.command()
def discovery(subnet: str, update_hosts: bool = typer.Option(False, "--update-hosts", "-u")):
    hosts = check_token()
    ipa = check_network(subnet)
    found_hosts = []

    if not ipa:
        err("Please setup a valid network: {}".format(subnet))
    for h in ipa.hosts():
        vuln_client = VulnClient(str(h), hosts.token)
        # log("ping {}".format(h))
        if vuln_client.ping():
            success("{} is a vuln-node!".format(str(h)))
            found_hosts.append(str(h))
    log("Found hosts : {}".format(found_hosts))
    if update_hosts: 
        log("Update hosts")
        for hh in found_hosts:
            hosts.add_host(hh)
        hosts.update()
        success("hosts.json updated!")

@typer_app.command()
def generate_vulnenv(no_vulns: int):
    hosts = check_token()
    vulhubs = find_vuln_projects(vuln_home(), True)
    vuln_env = Vulnenv(vulhubs)
    try:
        for h in hosts.envs.keys():
            vuln_env.create_env(h, no_vulns)

    except Exception as e:
        err(e)
    hosts.envs = vuln_env.envs
    hosts.update()
    success("vulnerable environments created in hosts.json ")

@typer_app.command()
def run_env(host: str):
    h = check_token()
    vuln_client = VulnClient(host, h.token)
    envs = h.envs
    env_host = envs.get(host)
    if not env_host:
        err("vulnenv not found for {}".format(host))
    vuln_client.run(env_host) 

@typer_app.command()
def run_envs():
    h = check_token()
    envs = h.envs
    hosts = envs.keys()
    for host in hosts: 
        env_host = envs.get(host)
        vuln_client = VulnClient(host, h.token)
        vuln_client.run(env_host)
    
@typer_app.command()
def down_envs():
    h = check_token()
    envs = h.envs
    hosts = envs.keys()
    for host in hosts: 
        env_host = envs.get(host)
        vuln_client = VulnClient(host, h.token)
        vuln_client.down(env_host)

@typer_app.command()
def ping(ip: str):
    h = check_token()
    vuln_client = VulnClient(ip, h.token)
    is_node = vuln_client.ping()
    if is_node:
        success("{} is a vuln-node!".format(ip))
    else:
        log("vuln-node not found")
