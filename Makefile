POETRY_RUN=poetry run
RM=rm -rf

build: 
	$(RM) dist/
	poetry build
push: build
	$(POETRY_RUN) twine upload dist/*