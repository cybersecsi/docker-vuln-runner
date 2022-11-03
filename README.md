<h1 align="center">
  <br>
    <img src="https://raw.githubusercontent.com/cyberscsi/docker-vuln-runner/main/logo.png" alt= "Docker Vuln Runner" width="300px">
</h1>
<p align="center">
    <b>Docker Vuln Runner</b> <br />
    A Docker runner for docker-based vulnerable environments. 
<p>
<p align="center">
  <a href="https://github.com/cybersecsi/docker-vuln-runner/blob/main/README.md"><img src="https://img.shields.io/badge/Documentation-complete-green.svg?style=flat"></a>
  <a href="https://github.com/cybersecsi/docker-vuln-runner/blob/main/LICENSE.md"><img src="https://img.shields.io/badge/License-GNU%20GPL-blue"></a>
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
``vuln-runner``  is a tool that allows you to quickly run the docker vulnerable stacks. 

The vulnerable stack actually supported are: 
* [vulhub repo](https://github.com/vulhub/vulhub)

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

* **Initialized the vulnerable environment:**  
```
vuln-runner init
```

[![asciicast](https://asciinema.org/a/nYJEd62OzL3WLUuigyjeChLIE.svg)](https://asciinema.org/a/nYJEd62OzL3WLUuigyjeChLIE)


* **List the vulnerable stacks:**
```
vuln-runner list
```  


[![asciicast](https://asciinema.org/a/raziKJLlR6vWSbiIwY1w8kqaq.svg)](https://asciinema.org/a/raziKJLlR6vWSbiIwY1w8kqaq)  

* **Run a list of vulnerable stacks:**

```
vuln-runner run vulhub.CVE-2014-3120,vulhub.CVE-2018-1270
```

[![asciicast](https://asciinema.org/a/wIOCYSrD9o5ZE6NmuCWLTTD8A.svg)](https://asciinema.org/a/wIOCYSrD9o5ZE6NmuCWLTTD8A)  


* **Down the list of vulnerable stacks:**
```
vuln-runner down vulhub.CVE-2014-3120,vulhub.CVE-2018-1270
```

[![asciicast](https://asciinema.org/a/fAuTCMJHdxa5sRK0VlbfAKqcV.svg)](https://asciinema.org/a/fAuTCMJHdxa5sRK0VlbfAKqcV)  

### Advanced usage: vulnerable environment  
With the previous commands you can already manage your vulnerable stacks and manually run and stop them. 
Anyway, you can also create *vulnerable environments*. 
A vulnerable environment is a set of vulnerable docker-compose stacks that has not ports' conflicts.   
You can generate a vulnerable environment descriptor in JSON format with the `generate-vulnenv` command:   
``` 
vuln-runner generate-vulnenv NO_VULNS [--no-env=<default=1>]
```  

* `NO_VULNS` defines the number of vulnerable stacks for each environment. 
* `--no-env` defines the number of environments. It is useful if you want to run vuln-runner in different hosts, where each host runs a single environment.   

For example, to create a JSON vulnerable descriptor with two vulnerable stack and two environments: 
```
vuln-runner generate-vulnenv 2 --no-env=2  
```

[![asciicast](https://asciinema.org/a/KxRWBVOMLymUQiWgjDDm4f6JS.svg)](https://asciinema.org/a/KxRWBVOMLymUQiWgjDDm4f6JS)   

You can output into the JSON descriptor into a file an reuse with two commands: 
* **run-env**: run the set of stacks belonging to a vulnerable environment.   
```
vuln-runner run-env output.json 1
```
[![asciicast](https://asciinema.org/a/vuL2l5vL8bqRefx9EAqYlqxFC.svg)](https://asciinema.org/a/vuL2l5vL8bqRefx9EAqYlqxFC)

* **down-env**: down the vulnerable environment.  

```
vuln-runner down-env output.json 1
```
[![asciicast](https://asciinema.org/a/fAuTCMJHdxa5sRK0VlbfAKqcV.svg)](https://asciinema.org/a/fAuTCMJHdxa5sRK0VlbfAKqcV)  


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


## Remote mode  
It is possible to use `vuln-runner` in distributed node: 
1. A *vuln-node* initializes a token and run a tcp server that listens for commands  
2. A *vuln-controller* starts the vulnerable environments   

### node configuration   
Initializes the node: 
 
```  
vuln-runner init 
vuln-node init 
```
You have to define a token that will be used to validate the requests that comes from a controller. 

Start the vulnerable node: 
```  
vuln-node start  
```   
The `vuln-node` listens for connections on port **4545** .  
When a vuln-node is listening for a connection the controlle is able to find it through the **discovery** step. 


### controller configuration  
Initialize the controller  
```  
vuln-runner init 
vuln-controller init 
```   

Discovery the remote nodes  
```   
vuln-controller discovery <subnet_vulnerable_nodes> -u  
```  
The `-u` option updates the `hosts.json` configuration file present in the ~/.vulnenv folder .  

When you have configured the `hosts.json` it is possible to generate a vulnerable environment configuration composed of `<no_env>` vulnerable scenarios. For example, the following command: 
```  
vuln-controller generate-vulnenv 2  
```

generates two vulnerable environment for each `vuln-node` discovered previosly.     

### Design considerations for the distributed architecture  
The token is used to authenticate the requests that comes from the controller. It is not used as secure mechanism. 
All the protocol is unencrypted, as we suppose that the environment is "unsecure-by-default". It is used to setup vulnerable machines. An attacker could potentially intercepts the requests and put them down. 

You could setup firewall rules to allow the connections to the **4545** only from the controller IP host. 

This is useful as the students should not be able to see that port. 

## Credits
Developed by gx1 [@SecSI](https://secsi.io)

## License
*Docker Vuln Runner* is released under the [GPL LICENSE](https://github.com/cybersecsi/docker-vuln-runner/blob/main/LICENSE.md)
