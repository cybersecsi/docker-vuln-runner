from datetime import datetime
from gc import is_finalized
import glob
from os import path
import sys

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
        vuln-runner v0.1.5 - https://github.com/cybersecsi/docker-vuln-runner
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


