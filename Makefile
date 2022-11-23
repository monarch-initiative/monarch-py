src/monarch_py/datamodels/model.py: src/monarch_py/datamodels
	poetry run gen-pydantic $< > $@

.PHONY: install
install:
	poetry install

.PHONY: test
test: install
	poetry run python -m pytest --ignore=ingest_template

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
	poetry run flake8 --exit-zero --max-line-length 120 src tests/
	poetry run black --check --diff src tests
	poetry run isort --check-only --diff src tests

.PHONY: format
format:
	poetry run autoflake \
		--recursive \
		--remove-all-unused-imports \
		--remove-unused-variables \
		--ignore-init-module-imports \
		--in-place monarch_py tests
	poetry run isort src tests
	poetry run black src tests
