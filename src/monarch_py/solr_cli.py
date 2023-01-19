from pathlib import Path
import sys

import sh
import typer

from monarch_py.utilities.utils import check_for_solr

solr_app = typer.Typer()

SOLR_DATA = Path(__file__).parent / "data" / "solr"

@solr_app.command("download")
def download_solr():
    sh.wget("https://data.monarchinitiative.org/monarch-kg-dev/latest/solr.tar.gz", "-O", "solr.tar.gz", _out=sys.stdout, _err=sys.stderr)
    sh.mkdir("-p", SOLR_DATA)
    sh.tar("-zxf", "solr.tar.gz", "-C", f"{SOLR_DATA}", _out=sys.stdout, _err=sys.stderr)
    sh.rm("solr.tar.gz")
    sh.chmod('-R','a+rwx', SOLR_DATA)

@solr_app.command("start")
def start_solr():
    # TODO: smarter check if any solr image is running, not just monarch solr? 

    import docker
    
    data = Path(SOLR_DATA) / 'data'
    
    dc = docker.from_env()

    c = check_for_solr()
    if not c:
        try:
            c = dc.containers.run(
                    "solr:8",
                    ports={'8983':8983},
                    volumes=[f'{data}:/opt/solr-data'],
                    environment=["SOLR_HOME=/opt/solr-data"],
                    name="monarch_solr",
                    command="",
                    detach=True,
                )
            print(f"{c.name} {c.status}")
        except Exception as e:
            print(f"Error instantiating monarch solr container: {e}")
    else:
        # print(f"{c.name} {c.status}")
        try:
            c.start()
        except Exception as e:
            print(f"Error running existing container {c.name} ({c.status}) - {e}")
            

@solr_app.command("stop")
def stop_solr():
    sh.docker.stop("monarch_solr")
    sh.docker.rm("monarch_solr")


@solr_app.command("remove")
def delete_solr():
    sh.rm("-rf", SOLR_DATA)


@solr_app.command("status")
def check_solr_status():
    c = check_for_solr()
    if not c:
        print("""
No monarch_solr container found. 

Download the Monarch Solr KG and start a local solr instance:
    monarch solr download
    monarch solr start
""")
    else:
        print(f"""
Found monarch_solr container: {c.id}
Container status: {c.status}
        """)
        if c.status == 'exited':
            print("Start the container using:\n\tmonarch solr start\n")
        if c.status == 'running':
            print("You can create a new container with\n\tmonarch solr stop\n\tmonarch solr start\n")

