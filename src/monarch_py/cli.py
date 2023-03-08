import importlib
from pathlib import Path

import typer

from monarch_py import solr_cli, sql_cli
# from monarch_py.solr_cli import associations as solr_associations
# from monarch_py.solr_cli import entity as solr_entity
# from monarch_py.solr_cli import search as solr_search
# from monarch_py.solr_cli import solr_app
# from monarch_py.sql_cli import sql_app

app = typer.Typer()
app.add_typer(solr_cli.solr_app, name="solr")
app.add_typer(sql_cli.sql_app, name="sql")


@app.command("schema")
def schema():
    """
    Print the linkml schema for the data model
    """
    schema_name = "model"
    schema_dir = Path(
        importlib.util.find_spec(f"monarch_py.datamodels.{schema_name}").origin
    ).parent
    schema_path = schema_dir / Path(schema_name + ".yaml")
    with open(schema_path, "r") as schema_file:
        print(schema_file.read())
    typer.Exit()

@app.command("entity")
def entity(
    id: str = typer.Option(None, "--id"),
    fmt: str = typer.Option("json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"),
    output: str = typer.Option(None, "--output", "-o", help="The path to the output file"),
    ):
    """
    Retrieve an entity by ID

    Args:
        id: The identifier of the entity to be retrieved
        fmt: The format of the output (TSV, YAML, JSON)
        output: The path to the output file (stdout if not specified)

    """
    solr_cli.entity(id, fmt, output)


@app.command("associations")
def associations(
    category: str = typer.Option(None, "--category", "-c"),
    subject: str = typer.Option(None, "--subject", "-s"),
    predicate: str = typer.Option(None, "--predicate", "-p"),
    object: str = typer.Option(None, "--object", "-o"),
    entity: str = typer.Option(None, "--entity", "-e"),
    between: str = typer.Option(None, "--between"),
    limit: int = typer.Option(20, "--limit", "-l"),
    offset: int = typer.Option(0, "--offset"),
    fmt: str = typer.Option("json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"),
    output: str = typer.Option(None, "--output", "-o", help="The path to the output file"),
):
    """
    Paginate through associations

    Args:
        category: The category of the association
        predicate: The predicate of the association
        subject: The subject of the association
        object: The object of the association
        entity: The subject or object of the association
        limit: The number of associations to return
        offset: The offset of the first association to be retrieved
        fmt: The format of the output (TSV, YAML, JSON)
        output: The path to the output file (stdout if not specified)
    """
    # todo: add output_type as an option to support tsv, json, etc. Maybe also rich-cli tables?

    solr_cli.associations(**locals())


@app.command("search")
def search(
    q: str = typer.Option(None, "--query", "-q"),
    category: str = typer.Option(None, "--category"),
    taxon: str = typer.Option(None, "--taxon"),
    limit: int = typer.Option(20, "--limit"),
    offset: int = typer.Option(0, "--offset"),
    fmt: str = typer.Option("json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"),
    output: str = typer.Option(None, "--output", "-o", help="The path to the output file"),
):
    """
    Search for entities

    Args:
        q: The query string to search for
        category: The category of the entity
        taxon: The taxon of the entity
        limit: The number of entities to return
        offset: The offset of the first entity to be retrieved
        fmt: The format of the output (TSV, YAML, JSON)
        output: The path to the output file (stdout if not specified)
    """
    solr_cli.search(**locals())


@app.command("histopheno")
def histopheno(
    subject: str = typer.Argument(None, help="The subject of the association"),
    fmt: str = typer.Option("json", "--format", "-f", help="The format of the output (TSV, YAML, JSON)"),
    output: str = typer.Option(None, "--output", "-o", help="The path to the output file")
):
    """
    Retrieve the histopheno data for an entity by ID

    Args:
        subject: The subject of the association

    Optional Args:
        fmt (str): The format of the output (TSV, YAML, JSON). Default JSON
        output (str): The path to the output file. Default stdout
    """
    solr_cli.histopheno(**locals())


if __name__ == "__main__":
    app()
