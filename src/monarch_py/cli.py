import importlib
from pathlib import Path
from typing import Optional, Literal

import typer

from monarch_py.implementations.solr.solr_implementation import SolrImplementation
from monarch_py.implementations.sql.sql_implementation import SQLImplementation

from monarch_py.solr_cli  import solr_app
from monarch_py.sql_cli import sql_app

from monarch_py.utilities.utils import check_for_data, check_for_solr

app = typer.Typer()
app.add_typer(solr_app, name="solr")
app.add_typer(sql_app, name='sql')
    
state = {"data-source": None}


def get_implementation(data_source: Optional[Literal['sql', 'solr']]):
    """Returns implementation of the specified data source"""

    # Check for data
    if not check_for_data(data_source):
        cont = typer.confirm(f"{data_source} data not found locally. Would you like to download?")
        if not cont:
            print("Please download the Monarch KG before proceeding.")
            typer.Abort()

    if data_source == "sql":
        return SQLImplementation()
    
    if data_source == 'solr':
        if not check_for_solr():
            pass
        pass


@app.command()
def test():
    """Temp function to test snippits of code before implementing"""
    print(check_for_solr())
    

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
def entity(data, id: str):
    """
    Retrieve an entity by ID

    Args:
        id: The identifier of the entity to be retrieved

    """
    data = get_implementation(data)

    entity = data.get_entity(id)
    print(entity.json(indent=4))


@app.command()
def associations(
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
    si = SolrImplementation()

    response = si.get_associations(
        category=category,
        predicate=predicate,
        subject=subject,
        object=object,
        entity=entity,
        limit=limit,
        offset=offset,
    )
    print(response.json(indent=4))



if __name__ == "__main__":
    app()
