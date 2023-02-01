import importlib
from pathlib import Path

import typer

from monarch_py.solr_cli import solr_app
from monarch_py.solr_cli import entity as solr_entity, associations as solr_associations, search as solr_search
from monarch_py.sql_cli import sql_app

app = typer.Typer()
app.add_typer(solr_app, name="solr")
app.add_typer(sql_app, name='sql')


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


@app.command("entity")
def entity(id: str = typer.Option(None, "--id")):
    """
    Retrieve an entity by ID

    Args:
        input: Which KG to use - solr or sql
        id: The identifier of the entity to be retrieved

    """
    solr_entity(id)
    

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
    """
    # todo: add output_type as an option to support tsv, json, etc. Maybe also rich-cli tables?

    solr_associations(**locals())


@app.command("search")
def search(
    q: str = typer.Option(None, "--query", "-q"),
    category: str = typer.Option(None, "--category"),
    taxon: str = typer.Option(None, "--taxon"),
    limit: int = typer.Option(20, "--limit"),
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
    solr_search(**locals())


if __name__ == "__main__":
    app()
