# docker-vulhub-runner
A docker runner for vulhub environment. 
<p align="center">
  <a href="https://github.com/cybersecsi/docker-vulhub-runner/blob/main/README.md"><img src="https://img.shields.io/badge/Documentation-complete-green.svg?style=flat"></a>
  <a href="https://github.com/cybersecsi/docker-vulhub-runner/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-GNU%20GPL-blue"></a>
</p>

## Table of Contents
- [Overview](#overview)
- [Install](#install)
- [Usage](#usage)
- [Demo](#demo)
- [Development](#development)
- [Credits](#credits)
- [License](#license)

## Overview
``docker-vulhub-rununer``  is a tool that allows you to quickly run the vulhub stacks present in the [vuhub repo](https://github.com/vulhub/vulhub).

At [SecSI](https://secsi.io) we found it useful to reproduce vulnerable environments for training purposes. Take a look at [DSP](https://secsi.io/docker-security-playground/).

## Install
You can easily install it by running:
```
pip install vulhub-runner
```

## Usage
```
vulhub-runner --help
```

This will display help for the tool. Here are all the switches it supports.

```

Usage: vulhub-runner [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  down
  down-env
  generate-vulnenv  Generate <no_env> vulnerable environments composed of...
  init
  list              List the vulhub cves
  run
  run-env
  update
```

## Demo
TBD  
## Development  
The [poetry](https://python-poetry.org/) packaging and management tool was used to build the project.  
To initialize the project: 
```
poetry install 
```  

To run the several commands, you can use poetry as follows:  
``` 
poetry run vulhub-runner <command> 
```  

## Credits
Developed by gx1 [@SecSI](https://secsi.io)

## License
*GPL* is released under the [GPL LICENSE](https://github.com/cybersecsi/docker-vulhub-runner/blob/main/LICENSE.md)
