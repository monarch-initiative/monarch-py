from pathlib import Path
from typing import Literal

import docker


def strip_json(doc: dict, *fields_to_remove: str):
    for field in fields_to_remove:
        try:
            del doc[field]
        except:
            pass
    return doc


def escape(value: str) -> str:
    return value.replace(":", "\:")


def check_for_data(data: Literal['solr', 'sql']):
    data_dir = Path(__file__).parent.parent / "data" / data
    return (data_dir.is_dir() and any(data_dir.iterdir()))


def check_for_solr():
    dc = docker.from_env()
    c = dc.containers.list(all=True, filters={"name":"monarch_solr"})
    return None if not c else c[0]

