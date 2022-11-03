POETRY_RUN=poetry run
RM=rm -rf

client-test:
	$(POETRY_RUN) vuln-controller ping 10.5.0.5

discovery-test:
	$(POETRY_RUN) vuln-controller discovery 10.5.0.0/24 -u

generate-controller-test:
	$(POETRY_RUN) vuln-controller generate-vulnenv 2

controller-run:
	$(POETRY_RUN) vuln-controller run-env 10.5.0.5
controller-run-all:
	$(POETRY_RUN) vuln-controller run-envs

controller-down-all:
	$(POETRY_RUN) vuln-controller down-envs
controller-norun:
	$(POETRY_RUN) vuln-controller run-env 10.5.0.9

controller-init:
	$(POETRY_RUN) vuln-controller init

node-init:
	$(POETRY_RUN) vuln-node init

node-run:
	$(POETRY_RUN) vuln-node run

build: 
	$(RM) dist/
	poetry build
push: build
	$(POETRY_RUN) twine upload dist/*