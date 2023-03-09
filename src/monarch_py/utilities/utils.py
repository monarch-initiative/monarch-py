import sys
import csv, yaml

import docker

from monarch_py.datamodels.model import ConfiguredBaseModel, Entity, Results

SOLR_DATA_URL = "https://data.monarchinitiative.org/monarch-kg-dev/latest/solr.tar.gz"
SQL_DATA_URL = "https://data.monarchinitiative.org/monarch-kg-dev/latest/monarch-kg.db.gz"


def strip_json(doc: dict, *fields_to_remove: str):
    for field in fields_to_remove:
        try:
            del doc[field]
        except:
            pass
    return doc


def escape(value: str) -> str:
    return value.replace(":", "\:")


def check_for_solr():
    print("\nChecking for solr container...")
    dc = docker.from_env()
    c = dc.containers.list(all=True, filters={"name": "monarch_solr"})
    return None if not c else c[0]


def dict_factory(cursor, row):
    """Converts a sqlite3 row to a dictionary."""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

### Output conversion methods ###

def to_json(obj: ConfiguredBaseModel, file: str):
    """Converts a pydantic model to a JSON string."""
    if file:
        with open(file, "w") as f:
            f.write(obj.json(indent=4))
        print(f"\nOutput written to {file}\n")
    else:
        print(obj.json(indent=4))


def to_tsv(obj: ConfiguredBaseModel, file: str) -> str:
    """Converts a pydantic model to a TSV string."""

    fh = open(file, "w") if file else sys.stdout
    writer = csv.writer(fh, delimiter="\t")

    if isinstance(obj, Entity):
        d = obj.dict()
        headers = d.keys()
        writer.writerow(headers)
        writer.writerow(d.values())
    elif isinstance(obj, Results):
        headers = obj.items[0].dict().keys()
        writer.writerow(headers)
        for item in obj.items:
            writer.writerow(item.dict().values())
    else:
        raise TypeError("Text conversion method only accepts Entity or Results objects.")

    if file: 
        fh.close()
        print(f"\nOutput written to {file}\n")
    
    return

def to_yaml(obj: ConfiguredBaseModel, file: str):
    """Converts a pydantic model to a YAML string."""
    
    fh = open(file, "w") if file else sys.stdout
    
    if isinstance(obj, Entity):
        d = obj.dict()
        yaml.dump(d, fh, indent=4)
    elif isinstance(obj, Results):
        d = [item.dict() for item in obj.items]
        yaml.dump(d, fh, indent=4)
    else:
        raise TypeError("YAML conversion method only accepts Entity or Results objects.")
    
    if file:
        print(f"\nOutput written to {file}\n")
        fh.close()

    return
