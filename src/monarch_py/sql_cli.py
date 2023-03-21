import typer

from monarch_py.implementations.sql.sql_implementation import SQLImplementation
from monarch_py.utils.utils import console, to_json, to_tsv, to_yaml

sql_app = typer.Typer()


@sql_app.command()
def entity(
    id: str = typer.Argument(None, help="The identifier of the entity to be retrieved"),
    update: bool = typer.Option(
        False, "--update", "-u", help="Whether to re-download the Monarch KG"
    ),
    fmt: str = typer.Option(
        "json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="The path to the output file"
    ),
):
    """Retrieve an entity by ID

    Args:
        id (str): The identifier of the entity to be retrieved
        update (bool): = Whether to re-download the Monarch KG. Default False
        fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
        output (str): The path to the output file. Default stdout
    """

    if not id:
        console.print("\n[bold red]Entity ID required.[/]\n")
        raise typer.Exit(1)

    data = SQLImplementation()
    response = data.get_entity(id, update)

    if not response:
        console.print(f"\nEntity '{id}' not found.\n")
        raise typer.Exit(1)

    if fmt == "json":
        to_json(response, output)
    elif fmt == "tsv":
        to_tsv(response, output)
    elif fmt == "yaml":
        to_yaml(response, output)
    else:
        console.print(f"\n[bold red]Format '{fmt}' not supported.[/]\n")
        raise typer.Exit(1)
    raise typer.Exit()


@sql_app.command()
def associations(
    category: str = typer.Option(None, "--category"),
    subject: str = typer.Option(None, "--subject"),
    predicate: str = typer.Option(None, "--predicate"),
    object: str = typer.Option(None, "--object"),
    entity: str = typer.Option(None, "--entity"),
    between: str = typer.Option(None, "--between"),
    limit: int = typer.Option(20, "--limit"),
    offset: int = typer.Option(0, "--offset"),
    update: bool = typer.Option(False, "--update"),
    fmt: str = typer.Option(
        "json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"
    ),
    output: str = typer.Option(
        None, "--output", "-o", help="The path to the output file"
    ),
):
    """Paginate through associations

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
    args.pop("fmt", None)
    args.pop("output", None)

    data = SQLImplementation()
    response = data.get_associations(**args)

    if fmt == "json":
        to_json(response, output)
    elif fmt == "tsv":
        to_tsv(response, output)
    elif fmt == "yaml":
        to_yaml(response, output)
    else:
        console.print(f"\n[bold red]Format '{fmt}' not supported.[/]\n")
        raise typer.Exit(1)
    raise typer.Exit()
