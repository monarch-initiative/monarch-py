monarch_py/datamodels/entity.py: schema/entity.yaml
	poetry run gen-pydantic $< > $@

monarch_py/datamodels/association.py: schema/association.yaml
	poetry run gen-pydantic $< > $@

clobber:
	rm monarch_py/datamodels/entity.py
	rm monarch_py/datamodels/association.py
