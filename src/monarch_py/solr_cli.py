import pystow
import typer

from monarch_py.datamodels.model import AssociationCountList
from monarch_py.utils.solr_cli_utils import (
    check_solr_permissions,
    get_solr,
    solr_status,
    start_solr,
    stop_solr,
)
from monarch_py.utils.utils import console, to_json, to_tsv, to_yaml

solr_app = typer.Typer()
monarchstow = pystow.module("monarch")

### SOLR DOCKER COMMANDS ###


@solr_app.command("start")
def start(update: bool = False):
    """Starts a local Solr container."""
    check_solr_permissions(update=False)
    start_solr()


@solr_app.command("stop")
def stop():
    """Stops the local Solr container."""
    stop_solr()
    raise typer.Exit()


@solr_app.command("status")
def status():
    solr_status()
    raise typer.Exit()


@solr_app.command("download")
def download():
    get_solr(update=True)
    raise typer.Exit()


### SOLR QUERY COMMANDS ###


@solr_app.command("entity")
def entity(
    id: str = typer.Argument(None, help="The identifier of the entity to be retrieved"),
    fmt: str = typer.Option(
        "json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="The path to the output file"
    ),
):
    """
    Retrieve an entity by ID

    Args:
        id (str): The identifier of the entity to be retrieved

    Optional Args:
        fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
        output (str): The path to the output file. Default stdout
    """

    if not id:
        console.print("\n[bold red]Entity ID required.[/]\n")
        raise typer.Exit(1)

    data = get_solr(update=False)
    response = data.get_entity(id)

    if fmt == "json":
        to_json(response, output)
    elif fmt == "tsv":
        to_tsv(response, output)
    elif fmt == "yaml":
        to_yaml(response, output)
    else:
        console.print(f"\n[bold red]Format '{fmt}' not supported.[/]\n")
    raise typer.Exit()


@solr_app.command("associations")
def associations(
    category: str = typer.Option(None, "--category"),
    subject: str = typer.Option(None, "--subject"),
    predicate: str = typer.Option(None, "--predicate"),
    object: str = typer.Option(None, "--object"),
    entity: str = typer.Option(None, "--entity"),
    between: str = typer.Option(None, "--between"),
    direct: bool = typer.Option(False, "--direct"),
    association_type: str = typer.Option(None, "--label"),
    limit: int = typer.Option(20, "--limit"),
    offset: int = typer.Option(0, "--offset"),
    fmt: str = typer.Option(
        "json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="The path to the output file"
    ),
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
        direct (bool, optional): Exclude associations with the specified subject and objects as ancestors. Default False
        association_type (str, optional): The association label of the association
        limit (int, optional): The number of associations to return. Default 20
        offset (int, optional): The offset of the first association to be retrieved. Default 0
        fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
        output (str): The path to the output file. Default stdout
    """
    args = locals()
    args.pop("update", None)
    args.pop("fmt", None)
    args.pop("output", None)

    data = get_solr(update=False)
    response = data.get_associations(**args)

    if fmt == "json":
        to_json(response, output)
    elif fmt == "tsv":
        to_tsv(response, output)
    elif fmt == "yaml":
        to_yaml(response, output)
    else:
        console.print(f"\n[bold red]Format '{fmt}' not supported.[/]\n")
    raise typer.Exit()


@solr_app.command("search")
def search(
    q: str = typer.Option(None, "--query", "-q"),
    category: str = typer.Option(None, "--category", "-c"),
    taxon: str = typer.Option(None, "--taxon", "-t"),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = typer.Option(0, "--offset"),
    fmt: str = typer.Option(
        "json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="The path to the output file"
    ),
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
    data = get_solr(update=False)

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
        console.print(f"\n[bold red]Format '{fmt}' not supported.[/]\n")
    raise typer.Exit()


@solr_app.command("autocomplete")
def autocomplete(
    q: str = typer.Argument(None, help="Query string to autocomplete against"),
    fmt: str = typer.Option(
        "json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="The path to the output file"
    ),
):
    """
    Return entity autcomplete matches for a query string

    Args:
        q: The query string to autocomplete against
        fmt: The format of the output (TSV, YAML, JSON)
        output: The path to the output file (stdout if not specified)

    """

    data = get_solr(update=False)
    response = data.autocomplete(q)

    if fmt == "json":
        to_json(response, output)
    elif fmt == "tsv":
        to_tsv(response, output)
    elif fmt == "yaml":
        to_yaml(response, output)
    else:
        console.print(f"\n[bold red]Format '{fmt}' not supported.[/]\n")
    raise typer.Exit()


@solr_app.command("histopheno")
def histopheno(
    subject: str = typer.Argument(None, help="The subject of the association"),
    fmt: str = typer.Option(
        "json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="The path to the output file"
    ),
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
        console.print("\n[bold red]Subject ID required.[/]\n")
        raise typer.Exit(1)

    data = get_solr(update=False)
    response = data.get_histopheno(subject)

    if fmt == "json":
        to_json(response, output)
    elif fmt == "tsv":
        to_tsv(response, output)
    elif fmt == "yaml":
        to_yaml(response, output)
    else:
        console.print(f"\n[bold red[Format '{fmt}' not supported.[/]\n")
    raise typer.Exit()


@solr_app.command("association-counts")
def association_counts(
    entity: str = typer.Argument(None, help="The entity to get association counts for"),
    fmt: str = typer.Option(
        "json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="The path to the output file"
    ),
):
    """
    Retrieve the association counts for a given entity

    Args:
        entity (str): The entity to get association counts for

    Optional Args:
        update (bool): Whether to re-download the Monarch KG. Default False
        fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
        output (str): The path to the output file. Default stdout
    """

    if not entity:
        console.print("\n[bold red]Entity ID required.[/]\n")
        raise typer.Exit(1)

    data = get_solr(update=False)
    response = data.get_association_counts(entity)
    counts = AssociationCountList(items=response)
    if fmt == "json":
        to_json(counts, output)
    elif fmt == "tsv":
        to_tsv(counts, output)
    elif fmt == "yaml":
        to_yaml(counts, output)
    else:
        console.print(f"\n[bold red[Format '{fmt}' not supported.[/]\n")
    raise typer.Exit()
