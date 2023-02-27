RUN = poetry run

src/monarch_py/datamodels/model.py: src/monarch_py/datamodels/model.yaml
	$(RUN) gen-pydantic $< > $@

.PHONY: install
install:
	poetry install

.PHONY: test
test: install
	$(RUN) python -m pytest --ignore=ingest_template


.PHONY: generate-docs
generate-docs: install
	$(RUN) gen-doc -d docs/Data-Model/ src/monarch_py/datamodels/model.yaml
	$(RUN) typer src/monarch_py/cli.py utils docs > docs/Usage/CLI.md

.PHONY: clobber
clobber:
	rm src/monarch_py/datamodels/model.py

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -rf .pytest_cache
	rm -rf dist

.PHONY: lint
lint:
	$(RUN) flake8 --exit-zero --max-line-length 120 src tests/
	$(RUN) black --check --diff src tests
	$(RUN) isort --check-only --diff src tests

.PHONY: format
format:
	$(RUN) autoflake \
		--recursive \
		--remove-all-unused-imports \
		--remove-unused-variables \
		--ignore-init-module-imports \
		--in-place src tests
	$(RUN) isort src tests
	$(RUN) black src tests
