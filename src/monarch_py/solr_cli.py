from typing import List

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
from monarch_py.utils.utils import console, format_output

solr_app = typer.Typer()
monarchstow = pystow.module("monarch")

############################
### SOLR DOCKER COMMANDS ###
############################


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
    """Checks the status of the local Solr container."""
    solr_status()
    raise typer.Exit()


@solr_app.command("download")
def download():
    """Download the Monarch Solr KG."""
    get_solr(update=True)
    raise typer.Exit()


###########################
### SOLR QUERY COMMANDS ###
###########################


@solr_app.command("entity")
def entity(
    id: str = typer.Argument(None, help="The identifier of the entity to be retrieved"),
    fmt: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="The format of the output (json, yaml, tsv, table)",
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
        fmt (str): The format of the output (json, yaml, tsv, table). Default JSON
        output (str): The path to the output file. Default stdout
    """

    if not id:
        console.print("\n[bold red]Entity ID required.[/]\n")
        raise typer.Exit(1)

    data = get_solr(update=False)
    response = data.get_entity(id)
    format_output(fmt, response, output)


@solr_app.command("associations")
def associations(
    category: str = typer.Option(None, "--category"),
    subject: str = typer.Option(None, "--subject"),
    predicate: str = typer.Option(None, "--predicate"),
    object: str = typer.Option(None, "--object"),
    entity: str = typer.Option(None, "--entity"),
    between: str = typer.Option(None, "--between"),
    direct: bool = typer.Option(False, "--direct"),
    limit: int = typer.Option(20, "--limit"),
    offset: int = typer.Option(0, "--offset"),
    fmt: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="The format of the output (json, yaml, tsv, table)",
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
        limit (int, optional): The number of associations to return. Default 20
        offset (int, optional): The offset of the first association to be retrieved. Default 0
        fmt (str): The format of the output (json, yaml, tsv, table). Default JSON
        output (str): The path to the output file. Default stdout
    """
    args = locals()
    args.pop("update", None)
    args.pop("fmt", None)
    args.pop("output", None)

    data = get_solr(update=False)
    response = data.get_associations(**args)
    format_output(fmt, response, output)


@solr_app.command("search")
def search(
    q: str = typer.Option(None, "--query", "-q"),
    category: List[str] = typer.Option(None, "--category", "-c"),
    in_taxon: str = typer.Option(None, "--in-taxon", "-t"),
    facet_fields: List[str] = typer.Option(None, "--facet-fields", "-ff"),
    facet_queries: List[str] = typer.Option(None, "--facet-queries"),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = typer.Option(0, "--offset"),
    fmt: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="The format of the output (json, yaml, tsv, table)",
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="The path to the output file"
    ),
    # sort: str = typer.Option(None, "--sort", "-s"),
):
    """
    Search for entities

    Optional Args:
        q: The query string to search for
        category: The category of the entity
        taxon: The taxon of the entity
        facet_fields: The fields to facet on
        facet_queries: The queries to facet on
        limit: The number of entities to return
        offset: The offset of the first entity to be retrieved
        fmt (str): The format of the output (json, yaml, tsv, table). Default JSON
        output (str): The path to the output file. Default stdout
    """
    params = locals()
    params.pop("fmt", None)
    params.pop("output", None)

    data = get_solr(update=False)
    response = data.search(**params)
    format_output(fmt, response, output)


@solr_app.command("autocomplete")
def autocomplete(
    q: str = typer.Argument(None, help="Query string to autocomplete against"),
    fmt: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="The format of the output (json, yaml, tsv, table)",
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="The path to the output file"
    ),
):
    """
    Return entity autcomplete matches for a query string

    Args:
        q: The query string to autocomplete against
        fmt: The format of the output (json, yaml, tsv, table)
        output: The path to the output file (stdout if not specified)

    """
    data = get_solr(update=False)
    response = data.autocomplete(q)
    format_output(fmt, response, output)


@solr_app.command("histopheno")
def histopheno(
    subject: str = typer.Argument(None, help="The subject of the association"),
    fmt: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="The format of the output (json, yaml, tsv, table)",
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
        fmt (str): The format of the output (json, yaml, tsv, table). Default JSON
        output (str): The path to the output file. Default stdout
    """

    if not subject:
        console.print("\n[bold red]Subject ID required.[/]\n")
        raise typer.Exit(1)

    data = get_solr(update=False)
    response = data.get_histopheno(subject)
    format_output(fmt, response, output)


@solr_app.command("association-counts")
def association_counts(
    entity: str = typer.Argument(None, help="The entity to get association counts for"),
    fmt: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="The format of the output (json, yaml, tsv, table)",
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
        fmt (str): The format of the output (json, yaml, tsv, table). Default JSON
        output (str): The path to the output file. Default stdout
    """
    if not entity:
        console.print("\n[bold red]Entity ID required.[/]\n")
        raise typer.Exit(1)
    data = get_solr(update=False)
    response = data.get_association_counts(entity)
    counts = AssociationCountList(items=response)
    format_output(fmt, counts, output)


@solr_app.command("association-table")
def association_table(
    entity: str = typer.Argument(..., help="The entity to get associations for"),
    category: str = typer.Argument(
        ...,
        help="The association category to get associations for, ex. biolink:GeneToPhenotypicFeatureAssociation",
    ),
    q: str = typer.Option(None, "--query", "-q"),
    limit: int = typer.Option(5, "--limit", "-l"),
    offset: int = typer.Option(0, "--offset"),
    fmt: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="The format of the output (json, yaml, tsv, table)",
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="The path to the output file"
    ),
):
    data = get_solr(update=False)
    response = data.get_association_table(
        entity=entity, category=category, q=q, limit=limit, offset=offset
    )
    format_output(fmt, response, output)
