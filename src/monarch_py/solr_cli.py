from pathlib import Path
import sys

import docker
import sh
import typer

solr_app = typer.Typer()

SOLR_DATA = Path(__file__).parent / "data" / "solr"

@solr_app.command("download")
def get_solr():
    sh.wget("https://data.monarchinitiative.org/monarch-kg-dev/latest/solr.tar.gz", "-O", "solr.tar.gz", _out=sys.stdout, _err=sys.stderr)
    sh.mkdir("-p", SOLR_DATA)
    sh.tar("-zxf", "solr.tar.gz", "-C", f"{SOLR_DATA}", _out=sys.stdout, _err=sys.stderr)
    sh.rm("solr.tar.gz")

@solr_app.command("start")
def start_solr():

    data = Path(SOLR_DATA) / 'data'

    # TODO: Check if monarch_py image exists and/or is running?

    dc = docker.from_env()
    container_exists = dc.containers.list(all=True, filters={"name":"monarch_solr"})
    if len(container_exists) == 0:
        c = dc.containers.run(
            "solr:8",
            ports={'8983':8983},
            volumes=[f'{data}:/var/solr'],
            name="monarch_solr",
            # command="solr",
            # detach=True,
        )
        print(c)


@solr_app.command("stop")
def stop_solr():
    sh.docker.stop("monarch_solr")
    sh.docker.rm("monarch_solr")

@solr_app.command("remove")
def delete_solr():
    sh.rm("-rf", SOLR_DATA)

