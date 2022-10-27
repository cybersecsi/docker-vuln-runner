# docker-vuln-runner
A docker runner for docker-based vulnerable environments. 
<p align="center">
  <a href="https://github.com/cybersecsi/docker-vuln-runner/blob/main/README.md"><img src="https://img.shields.io/badge/Documentation-complete-green.svg?style=flat"></a>
  <a href="https://github.com/cybersecsi/docker-vuln-runner/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-GNU%20GPL-blue"></a>
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
``docker-vuln-runner``  is a tool that allows you to quickly run the docker vulnerable stacks. 

The vulnerable stack actually supported are: 
* [vuhub repo](https://github.com/vulhub/vulhub)

At [SecSI](https://secsi.io) we found it useful to reproduce vulnerable environments for training purposes. To reproduce vulnerable environment easily, take a look at [DSP](https://secsi.io/docker-security-playground/).

## Install
You can easily install it by running:
```
pip install vuln-runner
```

## Usage
```
vuln-runner --help
```

This will display help for the tool. Here are all the switches it supports.

```
Usage: vuln-runner [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  down              Down a list of vulnerable projects
  down-env          Down an environment
  generate-vulnenv  Generate <no_env> vulnerable environments composed of...
  init
  list              List the vulnerable names
  run               Run a list of vulnerable projects
  run-env           Run an environment taken from a JSON configuration file
  update            Update the vulnerable git repositories

```

## Demo
Init:   
[![asciicast](https://asciinema.org/a/wwbUs5LZ5g02qgwR9NojM4L2e.svg)](https://asciinema.org/a/wwbUs5LZ5g02qgwR9NojM4L2e)  


List: 
[![asciicast](https://asciinema.org/a/t9U7RatbEBLodBsogpnfy8uGA.svg)](https://asciinema.org/a/t9U7RatbEBLodBsogpnfy8uGA)


Run a list of compose:  


## Development  
The [poetry](https://python-poetry.org/) packaging and management tool was used to build the project.  
To initialize the project: 
```
poetry install 
```  

To run the several commands, you can use poetry as follows:  

``` 
poetry run vuln-runner <command>  
```



## Credits
Developed by gx1 [@SecSI](https://secsi.io)

## License
*GPL* is released under the [GPL LICENSE](https://github.com/cybersecsi/docker-vuln-runner/blob/main/LICENSE.md)
