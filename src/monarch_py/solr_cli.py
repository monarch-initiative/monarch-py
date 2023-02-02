import sys, time

import pystow
import typer

from monarch_py.implementations.solr.solr_implementation import SolrImplementation
from monarch_py.utilities.utils import check_for_solr, SOLR_DATA_URL


solr_app = typer.Typer()
monarchstow = pystow.module("monarch")


def get_solr(update):
    if not check_for_solr():
        cont = typer.confirm("\nNo monarch_solr container found. Would you like to create and run one?")
        if not cont:
            print("\nPlease run a local Monarch Solr instance before proceeding:\n\tmonarch solr start\n")
            sys.exit(1)
        print("Starting local Monarch Solr instance...")
        start_solr(update)
    return SolrImplementation()


@solr_app.command("start")
def start_solr(update: bool = typer.Option(False, "--update", "-u", help="Whether to re-download the Monarch KG.")):
    # TODO: Smart-Check if any Solr image is running, not just monarch solr? or on the same port? 
    import docker
    dc = docker.from_env()
    
    monarchstow.ensure_untar(url=SOLR_DATA_URL, force=update)
    data = monarchstow.join("solr", "data")
    
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
    import docker
    dc = docker.from_env()
    c = check_for_solr()
    if c:
        try:
            print("Stopping Monarch Solr container...")
            c.stop()
            c.remove()
        except Exception as e:
            print(e)
            raise typer.Exit(1)


@solr_app.command("remove")
def delete_solr():
    ...


@solr_app.command("status")
def check_solr_status():
    c = check_for_solr()
    if not c:
        print("""
No monarch_solr container found. 

Download the Monarch Solr KG and start a local solr instance:
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
def entity(
    id: str = typer.Option(None, "--id", help="The identifier of the entity to be retrieved"),
    update: bool = typer.Option(False, "--update", "-u", help="Whether to re-download the Monarch KG")
    ):
    """
    Retrieve an entity by ID

    Args:
        id (str): The identifier of the entity to be retrieved
        update (bool): = Whether to re-download the Monarch KG. Default False
    """
    data = get_solr(update)
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
    update: bool = typer.Option(False, "--update", "-u", help="Whether to re-download the Monarch KG")
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
    args.pop('update', None)

    data = get_solr(update)
    response = data.get_associations(**args)
    print(response.json(indent=4))


@solr_app.command("search")
def search(
    q: str = typer.Option(None, "--query", "-q"),
    category: str = typer.Option(None, "--category", "-c"),
    taxon: str = typer.Option(None, "--taxon", "-t"),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = typer.Option(0, "--offset"),
    update: bool = typer.Option(False, "--update", "-u", help="Whether to re-download the Monarch KG")
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
    data = get_solr(update)

    response = data.search(
        q=q, category=category, taxon=taxon, limit=limit, offset=offset
    )
    print(response.json(indent=4))

