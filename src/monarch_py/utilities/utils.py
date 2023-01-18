import os, sys
from pathlib import Path
from typing import Literal

import docker
import sh

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
    # is_solr = sh.docker.images('-q', 'solr:8', _out=sys.stdout, _err=os.devnull)
    check = sh.docker.ps('-a', '--filter', 'name=monarch_solr')
    return check
    # return False if is_solr == "" else True

