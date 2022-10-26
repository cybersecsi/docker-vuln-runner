from datetime import datetime
from gc import is_finalized
import glob
from os import path
import sys

from docker_vulhub_runner.vulhub import Vulhub



# Colors
SUCCESS_C = '\033[92m'
DEBUG_C = '\033[93m'
ERROR_C = '\033[91m'
BOLD = '\033[1m'
END_C = '\033[0m'

def banner(silent = False):
  if not silent:
    print(
        '''
        ███████╗███████╗ ██████╗███████╗██╗
        ██╔════╝██╔════╝██╔════╝██╔════╝██║
        ███████╗█████╗  ██║     ███████╗██║
        ╚════██║██╔══╝  ██║     ╚════██║██║
        ███████║███████╗╚██████╗███████║██║
        ╚══════╝╚══════╝ ╚═════╝╚══════╝╚═╝
        vulhub v0.1.5 - https://github.com/cybersecsi/docker-vulhub-runner
        ''')   

def log(msg, silent = False):
    if not silent:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"[{current_time}] - [LOG] - {msg}", flush=True)

def success(msg):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"{SUCCESS_C}[{current_time}] - [SUCCESS] - {msg}{END_C}", flush=True)

def err(msg):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"{ERROR_C}[{current_time}] - [ERROR] - {msg}{END_C}", flush=True)
    sys.exit(-1)

def bold(msg):
    print(f"{BOLD}{msg}{END_C}", flush=True)


def get_compose_name(full_path):
    return path.basename(path.normpath(path.dirname(full_path)))

def find_vulhub_projects(base_path):
    ret = []
    for filename in glob.iglob(path.join(base_path, '**/docker-compose.yml'), recursive=True):
        ret.append(Vulhub(get_compose_name(filename), filename))
    return ret

def run_vulhub(vulhubs, vulhub_name):
    if not Vulhub.contains(vulhubs, vulhub_name):
        err("{} vulhub not found".format(vulhub_name))

    vulhub_obj = Vulhub.find_by_name(vulhubs, vulhub_name)
    vulhub_obj.run()

def down_vulhub(vulhubs, vulhub_name):
    if not Vulhub.contains(vulhubs, vulhub_name):
        err("{} vulhub not found".format(vulhub_name))

    vulhub_obj = Vulhub.find_by_name(vulhubs, vulhub_name)
    vulhub_obj.down()

def get_ports(vulhubs, vulhub_name):
    if not Vulhub.contains(vulhubs, vulhub_name):
        err("{} vulhub not found".format(vulhub_name))
    vulhub_obj = Vulhub.find_by_name(vulhubs, vulhub_name)
    return vulhub_obj.ports()

def check_init():
    if not Vulhub.is_initialized():
        err("{} does not exist, please run \"vulhub-runner init\" first".format(Vulhub.home()))