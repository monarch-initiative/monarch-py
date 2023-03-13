import os, sys
import time

import pystow
import typer

from monarch_py.implementations.solr.solr_implementation import SolrImplementation
from monarch_py.utilities.utils import SOLR_DATA_URL, check_for_solr, to_tsv, to_yaml, to_json

solr_app = typer.Typer()
monarchstow = pystow.module("monarch")
    

def get_solr(update):

    if sys.platform in ["linux", "linux2"]:
        import stat

        stat_info = os.stat(monarchstow.base)
        if (stat_info.st_uid != 8983 or
            stat_info.st_gid != 8983):
            print(f"""
Solr container requires write access to {monarchstow.base}.
Please run the following command to fix permissions:
    sudo chown -R 8983:8983 {monarchstow.base}
    sudo chmod -R g+w {monarchstow.base}
""")

    if not check_for_solr():
        cont = typer.confirm(
            "\nNo monarch_solr container found. Would you like to create and run one?"
        )
        if not cont:
            print(
                "\nPlease run a local Monarch Solr instance before proceeding:\n\tmonarch solr start\n"
            )
            sys.exit(1)
        print("Starting local Monarch Solr instance...")
        start_solr(update)

    return SolrImplementation()


### Solr Docker Commands ###

@solr_app.command("start")
def start_solr(
    update: bool = typer.Option(False, "--update", "-u", help="Whether to re-download the Monarch KG.")
    ):
    """Start a local Monarch Solr instance."""

    import docker

    dc = docker.from_env()

    monarchstow.ensure_untar(url=SOLR_DATA_URL, force=update)
    data = monarchstow.join("solr", "data")

    c = check_for_solr()
    if not c:
        try:
            c = dc.containers.run(
                "solr:8",
                ports={"8983": 8983},
                volumes=[f"{data}:/opt/solr-data"],
                environment=["SOLR_HOME=/opt/solr-data"],
                name="monarch_solr",
                command="",
                detach=True,
            )
            time.sleep(10)
            print(f"{c.name} {c.status}")
        except Exception as e:
            print(f"Error instantiating monarch solr container: {e}")
            raise typer.Exit(1)
    else:
        try:
            c.start()
        except Exception as e:
            print(f"Error running existing container {c.name} ({c.status}) - {e}")
            raise typer.Exit(1)
    typer.Exit()

@solr_app.command("stop")
def stop_solr():
    """Stop the local Monarch Solr instance."""
    import docker

    docker.from_env()
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
    """Check the status of the local Monarch Solr instance."""
    c = check_for_solr()
    if not c:
        print(
            """
No monarch_solr container found. 

Download the Monarch Solr KG and start a local solr instance:
    monarch solr start
"""
        )
    else:
        print(
            f"""
Found monarch_solr container: {c.id}
Container status: {c.status}
        """
        )
        if c.status == "exited":
            print("Start the container using:\n\tmonarch solr start\n")
        if c.status == "running":
            print(
                "You can create a new container with\n\tmonarch solr stop\n\tmonarch solr start\n"
            )


### Solr Query Commands ###

@solr_app.command("entity")
def entity(
    id: str = typer.Argument(None, help="The identifier of the entity to be retrieved"),
    update: bool = typer.Option(False, "--update", "-u", help="Whether to re-download the Monarch KG"),
    fmt: str = typer.Option("json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"),
    output: str = typer.Option(None, "--output", "-o", help="The path to the output file"),
    ):
    """
    Retrieve an entity by ID

    Args:
        id (str): The identifier of the entity to be retrieved

    Optional Args:
        update (bool): = Whether to re-download the Monarch KG. Default False
        fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
        output (str): The path to the output file. Default stdout
    """

    if not id:
        print("\nEntity ID required.\n")
        typer.Exit(1)

    data = get_solr(update)
    response = data.get_entity(id)
    
    if fmt == "json":
        to_json(response, output)
    elif fmt == "tsv":
        to_tsv(response, output)
    elif fmt == "yaml":
        to_yaml(response, output)
    else:
        print(f"\nFormat '{fmt}' not supported.\n")
    typer.Exit()


@solr_app.command("associations")
def associations(
    category: str = typer.Option(None, "--category"),
    subject: str = typer.Option(None, "--subject"),
    predicate: str = typer.Option(None, "--predicate"),
    object: str = typer.Option(None, "--object"),
    entity: str = typer.Option(None, "--entity"),
    between: str = typer.Option(None, "--between"),
    limit: int = typer.Option(20, "--limit"),
    offset: int = typer.Option(0, "--offset"),
    update: bool = typer.Option(False, "--update", "-u", help="Whether to re-download the Monarch KG"),
    fmt: str = typer.Option("json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"),
    output: str = typer.Option(None, "--output", "-o", help="The path to the output file"),
    ):
    """
    Paginate through associations

    Args:
        category (str, optional): The category of the association.
        subject (str, optional): The subject of the association.
        predicate (str, optional): The predicate of the association.
        object (str, optional): The object of the association.
        entity (str, optional): The subject or object of the association.
        between (str, optional): Two comma-separated entities to get bi-directional associations.
        limit (int, optional): The number of associations to return. Default 20
        offset (int, optional): The offset of the first association to be retrieved. Default 0
        update (bool, optional): Whether to re-download the Monarch KG. Default False
        fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
        output (str): The path to the output file. Default stdout
    """
    args = locals()
    args.pop("update", None)
    args.pop("fmt", None)
    args.pop("output", None)

    data = get_solr(update)
    response = data.get_associations(**args)

    if fmt == "json":
        to_json(response, output)
    elif fmt == "tsv":
        to_tsv(response, output)
    elif fmt == "yaml":
        to_yaml(response, output)
    else:
        print(f"\nFormat '{fmt}' not supported.\n")
    typer.Exit()


@solr_app.command("search")
def search(
    q: str = typer.Option(None, "--query", "-q"),
    category: str = typer.Option(None, "--category", "-c"),
    taxon: str = typer.Option(None, "--taxon", "-t"),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = typer.Option(0, "--offset"),
    update: bool = typer.Option(False, "--update", "-u", help="Whether to re-download the Monarch KG"),
    fmt: str = typer.Option("json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"),
    output: str = typer.Option(None, "--output", "-o", help="The path to the output file"),
    ):
    """
    Search for entities

    Optional Args:
        q: The query string to search for
        category: The category of the entity
        taxon: The taxon of the entity
        limit: The number of entities to return
        offset: The offset of the first entity to be retrieved
        fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
        output (str): The path to the output file. Default stdout
    """
    data = get_solr(update)

    response = data.search(
        q=q, category=category, taxon=taxon, limit=limit, offset=offset
    )
    
    if fmt == "json":
        to_json(response, output)
    elif fmt == "tsv":
        to_tsv(response, output)
    elif fmt == "yaml":
        to_yaml(response, output)
    else:
        print(f"\nFormat '{fmt}' not supported.\n")
    typer.Exit()


@solr_app.command("histopheno")
def histopheno(
    subject: str = typer.Argument(None, help="The subject of the association"),
    update: bool = typer.Option(False, "--update", "-u", help="Whether to re-download the Monarch KG"),
    fmt: str = typer.Option("json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"),
    output: str = typer.Option(None, "--output", "-o", help="The path to the output file")
    ):
    """
    Retrieve the histopheno associations for a given subject

    Args:
        subject (str): The subject of the association

    Optional Args:
        update (bool): Whether to re-download the Monarch KG. Default False
        fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
        output (str): The path to the output file. Default stdout
    """

    if not subject:
        print("\nSubject ID required.\n")
        typer.Exit(1)

    data = get_solr(update)
    response = data.get_histopheno(subject)
    
    if fmt == "json":
        to_json(response, output)
    elif fmt == "tsv":
        to_tsv(response, output)
    elif fmt == "yaml":
        to_yaml(response, output)
    else:
        print(f"\nFormat '{fmt}' not supported.\n")
    typer.Exit()
