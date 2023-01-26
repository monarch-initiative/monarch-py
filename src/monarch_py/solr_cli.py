from pathlib import Path
import sys
import time

import sh
import typer

from monarch_py.implementations.solr.solr_implementation import SolrImplementation
from monarch_py.utilities.utils import check_for_solr, check_for_data

solr_app = typer.Typer()

SOLR_DATA = Path(__file__).parent / "data" / "solr"


def get_solr():
    if not check_for_data('solr'):
        cont = typer.confirm(f"\nSolr data not found locally. Would you like to download?\n")
        if not cont:
            print("Please download the Monarch KG before proceeding.")
            typer.Abort()
        download_solr()

    if not check_for_solr():
        cont = typer.confirm("No monarch_solr container found. Would you like to create and run one?")
        if not cont:
            print("\nPlease run a local Monarch Solr instance before proceeding:\n\tmonarch solr start\n")
            typer.Abort()
        print("Starting local Monarch Solr instance...")
        start_solr()
    return SolrImplementation()


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
            time.sleep(10)
            print(f"{c.name} {c.status}")
        except Exception as e:
            print(f"Error instantiating monarch solr container: {e}")
    else:
        try:
            c.start()
            # print(f"{c.name} {c.status}")
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


@solr_app.command()
def entity(id: str = typer.Option(None, "--id")):
    """
    Retrieve an entity by ID

    Args:
        input: Which KG to use - solr or sql
        id: The identifier of the entity to be retrieved

    """
    data = get_solr()
    entity = data.get_entity(id)
    print(entity.json(indent=4))
    

@solr_app.command()
def associations(
    category: str = typer.Option(None, "--category"),
    subject: str = typer.Option(None, "--subject"),
    predicate: str = typer.Option(None, "--predicate"),
    object: str = typer.Option(None, "--object"),
    entity: str = typer.Option(None, "--entity"),
    between: str = typer.Option(None, "--between"),
    limit: int = typer.Option(20, "--limit"),
    offset: int = typer.Option(0, "--offset"),
    # todo: add output_type as an option to support tsv, json, etc. Maybe also rich-cli tables?
    ):
    """
    Paginate through associations

    Args:
        category: The category of the association
        predicate: The predicate of the association
        subject: The subject of the association
        object: The object of the association
        entity: The subject or object of the association
        between: Two comma-separated entities to get bi-directional associations
        limit: The number of associations to return
        offset: The offset of the first association to be retrieved
    """
    args = locals()
    data = get_solr()
    response = data.get_associations(**args)
    print(response.json(indent=4))


@solr_app.command("search")
def search(
    q: str = typer.Option(None, "--query", "-q"),
    category: str = typer.Option(None, "--category", "-c"),
    taxon: str = typer.Option(None, "--taxon", "-t"),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = typer.Option(0, "--offset"),
):
    """
    Search for entities

    Args:
        q: The query string to search for
        category: The category of the entity
        taxon: The taxon of the entity
        limit: The number of entities to return
        offset: The offset of the first entity to be retrieved
    """
    data = get_solr()

    response = data.search(
        q=q, category=category, taxon=taxon, limit=limit, offset=offset
    )
    print(response.json(indent=4))

