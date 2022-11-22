monarch_py/datamodels/model.py: schema/monarch-py.yaml
	poetry run gen-pydantic $< > $@

.PHONY: install
install:
	poetry install

.PHONY: test
test: install
	poetry run python -m pytest --ignore=ingest_template

.PHONY: clobber
clobber:
	rm monarch_py/datamodels/model.py

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -rf .pytest_cache
	rm -rf dist

.PHONY: lint
lint:
	poetry run flake8 --exit-zero --max-line-length 120 monarch_ingest/ tests/
	poetry run black --check --diff monarch_ingest tests
	poetry run isort --check-only --diff monarch_ingest tests

.PHONY: format
format:
	poetry run autoflake \
		--recursive \
		--remove-all-unused-imports \
		--remove-unused-variables \
		--ignore-init-module-imports \
		--in-place monarch_ingest tests
	poetry run isort monarch_ingest tests
	poetry run black monarch_ingest tests
