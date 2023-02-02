from typing import Literal

import docker
import pystow


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


def check_for_data(data: Literal['solr', 'sql']):
    data_dir = pystow.join("monarch", data)
    return (data_dir.is_dir() and any(data_dir.iterdir()))


def check_for_solr():
    dc = docker.from_env()
    c = dc.containers.list(all=True, filters={"name":"monarch_solr"})
    return None if not c else c[0]


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

