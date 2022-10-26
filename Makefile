POETRY=poetry run
VULHUB_RUNNER=$(POETRY) vulhub-runner
run:
	$(VULHUB_RUNNER)

test:
	$(POETRY) pytest -s -vv
