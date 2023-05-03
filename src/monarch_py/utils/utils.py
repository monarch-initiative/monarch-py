import csv
import sys

import yaml
from rich import print_json
from rich.console import Console
from rich.table import Table

from monarch_py.datamodels.model import (
    AssociationCountList,
    ConfiguredBaseModel,
    Entity,
    HistoPheno,
    Results,
)

SOLR_DATA_URL = "https://data.monarchinitiative.org/monarch-kg-dev/latest/solr.tar.gz"
SQL_DATA_URL = (
    "https://data.monarchinitiative.org/monarch-kg-dev/latest/monarch-kg.db.gz"
)


console = Console(
    color_system="truecolor",
    stderr=True,
    style="pink1",
)


def strip_json(doc: dict, *fields_to_remove: str):
    for field in fields_to_remove:
        try:
            del doc[field]
        except:
            pass
    return doc


def escape(value: str) -> str:
    return value.replace(":", r"\:")


def dict_factory(cursor, row):
    """Converts a sqlite3 row to a dictionary."""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


### Output conversion methods ###

FMT_INPUT_ERROR_MSG = "Text conversion method only accepts Entity, HistoPheno, AssociationCountList, or Results objects."


def get_headers_from_obj(obj: ConfiguredBaseModel) -> list:
    # example = list(type(obj).schema()['definitions'][type(obj).schema()['properties']['items']['items']['$ref'].split('/')[-1]]['properties'].keys())
    schema = type(obj).schema()
    definitions = schema['definitions']
    this_ref = schema['properties']['items']['items']['$ref'].split('/')[-1]
    headers = definitions[this_ref]['properties'].keys()
    return list(headers)


def to_json(obj: ConfiguredBaseModel, file: str):
    """Converts a pydantic model to a JSON string."""
    if file:
        with open(file, "w") as f:
            f.write(obj.json(indent=4))
        console.print(f"\nOutput written to {file}\n")
    else:
        print_json(obj.json(indent=4))


def to_tsv(obj: ConfiguredBaseModel, file: str) -> str:
    """Converts a pydantic model to a TSV string."""

    # Extract headers and rows from object
    if isinstance(obj, Entity):
        headers = obj.dict().keys()
        rows = [list(obj.dict().values())]
    elif isinstance(obj, (AssociationCountList, HistoPheno, Results)):
        if not obj.items:
            headers = get_headers_from_obj(obj)
            rows = []
        else:
            headers = obj.items[0].dict().keys()
            rows = [list(item.dict().values()) for item in obj.items]
    else:
        raise TypeError(FMT_INPUT_ERROR_MSG)

    if file: # Write to file
        fh = open(file, "w")
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(headers)
        for row in rows:
            writer.writerow(list(row))
        fh.close()
        console.print(f"\nOutput written to {file}\n")

    else: # Print to console
        for row in rows:
            for i, value in enumerate(row):
                if isinstance(value, list):
                    row[i] = ", ".join(value)
                elif not isinstance(value, str):
                    row[i] = str(value)
        title = (
            f"{obj.__class__.__name__}: {obj.id}"
            if hasattr(obj, "id")
            else obj.__class__.__name__
        )
        table = Table(
            title=console.rule(title),
            show_header=True,
            header_style="bold cyan",
        )
        for header in headers:
            table.add_column(header)
        for row in rows:
            table.add_row(*row)
        console.print(table)


def to_yaml(obj: ConfiguredBaseModel, file: str):
    """Converts a pydantic model to a YAML string."""

    fh = open(file, "w") if file else sys.stdout

    if isinstance(obj, Entity):
        yaml.dump(obj.dict(), fh, indent=4)
    elif (
        isinstance(obj, Results)
        or isinstance(obj, HistoPheno)
        or isinstance(obj, AssociationCountList)
    ):
        yaml.dump([item.dict() for item in obj.items], fh, indent=4)
    else:
        raise TypeError(FMT_INPUT_ERROR_MSG)

    if file:
        console.print(f"\nOutput written to {file}\n")
        fh.close()

    return
