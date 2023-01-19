import importlib
from pathlib import Path
from typing import Literal

import typer

from monarch_py.implementations.solr.solr_implementation import SolrImplementation
from monarch_py.implementations.sql.sql_implementation import SQLImplementation
from monarch_py.solr_cli import solr_app, start_solr, download_solr
from monarch_py.sql_cli import sql_app, download_sql
from monarch_py.utilities.utils import check_for_data, check_for_solr

app = typer.Typer()
app.add_typer(solr_app, name="solr")
app.add_typer(sql_app, name='sql')
    

def get_implementation(data_source: Literal['sql', 'solr']):
    """Returns implementation of the specified data source"""

    if not check_for_data(data_source):
        cont = typer.confirm(f"\n{data_source} data not found locally. Would you like to download?\n")
        if not cont:
            print("Please download the Monarch KG before proceeding.")
            typer.Abort()
        download_sql() if data_source == 'sql' else download_solr()

    if data_source == "sql":
        return SQLImplementation()
    
    if data_source == 'solr':
        if not check_for_solr():
            cont = typer.confirm("No monarch_solr container found. Would you like to create and run one?")
            if not cont:
                print("\nPlease run a local Monarch Solr instance before proceeding:\n\tmonarch solr start\n")
                typer.Abort()
        start_solr()
        return SolrImplementation()


# @app.command()
# def test():
#     """Temp function to test snippits of code before implementing"""
#     pass
    

@app.command()
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


@app.command()
def entity(
    source: str = typer.Option('solr', "--source"), 
    id: str = typer.Option(None, "--id")
    ):
    """
    Retrieve an entity by ID

    Args:
        source: Which KG to use - solr or sql
        id: The identifier of the entity to be retrieved

    """
    data = get_implementation(source)
    entity = data.get_entity(id)
    if source == 'solr':
        print(entity.json(indent=4))
    else:
        print(entity)


@app.command()
def associations(
    source: str = typer.Option('solr', "--source"),
    category: str = typer.Option(None, "--category", "-c"),
    subject: str = typer.Option(None, "--subject", "-s"),
    predicate: str = typer.Option(None, "--predicate", "-p"),
    object: str = typer.Option(None, "--object", "-o"),
    entity: str = typer.Option(None, "--entity", "-e"),
    limit: int = typer.Option(20, "--limit", "-l"),
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
        limit: The number of associations to return
        offset: The offset of the first association to be retrieved
    """
    data = get_implementation(source)

    response = data.get_associations(
        category=category,
        predicate=predicate,
        subject=subject,
        object=object,
        entity=entity,
        limit=limit,
        offset=offset,
    )
    print(response.json(indent=4))

@app.command("search")
def search(
    source: str = typer.Option('solr', "--source"),
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
    data = get_implementation(source)

    response = data.search(
        q=q, category=category, taxon=taxon, limit=limit, offset=offset
    )
    print(response.json(indent=4))


if __name__ == "__main__":
    app()
